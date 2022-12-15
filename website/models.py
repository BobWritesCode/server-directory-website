from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, 'Draft'), (1, 'Published'))

class ServerListing(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    short_description = models.TextField()
    long_description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="server_listings")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    logo = CloudinaryField('image', default='placeholder')
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name="server_likes", blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

