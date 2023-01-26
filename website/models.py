from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField

STATUS = ((0, 'Draft'), (1, 'Published'))


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

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
        Game, on_delete=models.CASCADE, related_name="server_listings")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="server_owner")
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    logo = CloudinaryField('image', default='placeholder')
    tags = models.ManyToManyField(Tag, blank=True)
    short_description = models.TextField(max_length=200)
    long_description = models.TextField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    discord = models.CharField(max_length=50)
    bumps = models.ManyToManyField(
        CustomUser, related_name="server_bumps", blank=True)
    last_bump = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_tags(self):
        return self.tags.count()

    def number_of_bumps(self):
        return self.bumps.count()

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
