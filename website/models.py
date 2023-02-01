from datetime import timedelta, date
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField

from .constants import DAYS_TO_EXPIRE_BUMP

STATUS = ((0, 'Draft'), (1, 'Published'))

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, blank=False)
    first_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, blank=False)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return f"{self.email}"

class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"


class Game(models.Model):
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=50, unique=True)
    tags = models.ManyToManyField(Tag, blank=False)
    image = CloudinaryField('image', default='placeholder', blank=False)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return f"{self.name}"


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
    long_description = models.TextField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    discord = models.CharField(max_length=50)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_tags(self):
        return self.tags.count()

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