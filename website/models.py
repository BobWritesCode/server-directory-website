from django.db import models
from django.contrib.auth.models import AbstractUser

from cloudinary.models import CloudinaryField
from datetime import timedelta, date
from tinymce import models as tinymce_models
import json

from .constants import DAYS_TO_EXPIRE_BUMP

STATUS = ((0, 'Draft'), (1, 'Published'))


class CustomUser(AbstractUser):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=20, unique=True, blank=False)
    first_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, blank=False)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return f"{self.email}"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class Tag(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class Game(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=50, unique=True)
    tags = models.ManyToManyField(Tag, blank=False)
    image = CloudinaryField('image', null=True, default=None, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return f"{self.name}"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class ServerListing(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="ServerListing")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="ServerListing")
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    logo = CloudinaryField('image', default='placeholder')
    tags = models.ManyToManyField(Tag, blank=True)
    short_description = models.TextField(max_length=200)
    long_description = tinymce_models.HTMLField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    discord = models.CharField(max_length=50)
    tiktok = models.CharField(default='', max_length=50, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    bump_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def bumpCount(self):
        return Bumps.objects.filter(listing=self.pk).count()

    def number_of_tags(self):
        return self.tags.count()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def save(self, *args, **kwargs):
        if self.pk:
            self.slug = f'Listing-{self.pk}'
        else:
            if ServerListing.objects.count() == 0:
                next_id = 1
            else:
                next_id = ServerListing.objects.order_by('-id').first().id + 1

            self.slug = f'Listing-{next_id}'
        super(ServerListing, self).save(*args, **kwargs)


class Bumps(models.Model):

    def set_expiry():
        return date.today() + timedelta(days=DAYS_TO_EXPIRE_BUMP)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    listing = models.ForeignKey(ServerListing, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    expiry = models.DateField(default=set_expiry(), blank=False)


class Images(models.Model):

    image = CloudinaryField('image', default='placeholder')
    public_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_uploaded")
    reviewed_by = models.ForeignKey(
        CustomUser,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="user_approved"
    )
    listing = models.ForeignKey(ServerListing, on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=(
            (0, 'Unapproved'),
            (1, 'Approved'),
            (2, 'Rejected'),
            (3, 'Rejected and User banned')
            ),
        default=0
        )
    date_added = models.DateField(auto_now_add=True)
    expiry = models.DateField(null=True, blank=True)