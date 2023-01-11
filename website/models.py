from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField

STATUS = ((0, 'Draft'), (1, 'Published'))

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
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="server_listings")
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    logo = CloudinaryField('image', default='placeholder')
    tags = models.ManyToManyField(Tag, blank=True)
    short_description = models.TextField(max_length=200)
    long_description = models.TextField(max_length=2000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="server_owner")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    discord =  models.CharField(max_length=50)
    likes = models.ManyToManyField(User, related_name="server_likes", blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_tags(self):
        return self.tags.count()

    def number_of_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        if self.pk:
            self.slug = f'Listing-{self.pk}'
        else:
            next_id = ServerListing.objects.order_by('-id').first().id + 1
            self.slug = f'Listing-{next_id}'
        super(ServerListing, self).save(*args, **kwargs)