"""
All models for app
"""
import uuid
import json
from datetime import timedelta, date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from cloudinary.models import CloudinaryField
from tinymce import models as tinymce_models

from .constants import DAYS_TO_EXPIRE_BUMP

STATUS = ((0, 'Draft'), (1, 'Published'))


class CustomUser(AbstractUser):
    """
    A class to represent a user.

    ...

    Attributes
    ----------
    username : str : REQUIRED
        Chosen by user to represent themselves.
    username_lower : str : REQUIRED
        Username converted to lowercase. To stop two usernames being the same
        just differing by case.
    first_name : str
        User's first name.
    email : str : USERNAME_FIELD
        User's primary email address.
    email_verified : bool
        Has use completed email verification.
    is_staff : bool
        Is the user a staff user.
    is_active : bool
        Can the user log in.
    is_banned : bool
        Has the account been banned.
    date_joined : datetime
        Date and time user originally signed up.

    Methods
    -------
    __str__():
        returns email address as the class str.

    to_json():
        converts class into a json string.

    save():
        Saves object. Also checks to make sure username is not already taken by
        checking converting username to lower case and comparing against
        username_lower.
    """

    username = models.CharField(
        max_length=20,
        blank=False,
        unique=True,
        error_messages={
            'unique': 'Username already taken. (Panda)', }
        )
    username_lower = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(
        max_length=50,
        default=None,
        null=True,
        blank=True)
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            'unique': 'Email already taken. (Cobra)', }
        )
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        """
        Returns email address as the class str.

        Args:
            None

        Returns:
            email: str
        """
        return f"{self.email}"

    def to_json(self):
        """
        Returns class as a JSON string.

        Args:
            None

        Returns:
            Class as a JSON: str
        """
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
            )

    def save(self, *args, **kwargs):
        """
        Save object after checking that their are no duplicates within
        username_lower or email.

        Args:
            None

        Returns:
            no return.
        """
        # Convert email address to lowercase to stop duplication.
        self.email = str(self.email).lower()
        # Convert username to lowercase to stop duplication.
        self.username_lower = str(self.username).lower()

        if not self.pk:
            # Adding a new object.
            existing_usernames = CustomUser.objects.filter(
                username_lower=self.username_lower)
            existing_emails = CustomUser.objects.filter(
                email=self.email)
        else:
            # Updating an existing object.
            existing_usernames = CustomUser.objects.filter(
                username_lower=self.username_lower).exclude(pk=self.pk)
            existing_emails = CustomUser.objects.filter(
                email=self.email).exclude(pk=self.pk)
        # If any duplicates create error messages and raise ValidationError
        if existing_emails or existing_usernames:
            errors = {}
            if existing_emails:
                errors['email'] = ['Email already taken. (Jackal)']
            if existing_usernames:
                errors['username'] = ['Username already taken. (Lion)']
            raise ValidationError(errors)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """
    A class to represent a tag for a listing and game.

    ...

    Attributes
    ----------
    name : str
        The tag name.
    slug : str
        The slug which is used in the url.

    Methods
    -------
    __str__():
        returns name as the class str.

    to_json():
        converts class into a json string.
    """
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        """
        Returns name as the class str.

        Args:
            None

        Returns:
            name: str
        """
        return f"{self.name}"

    def to_json(self):
        """
        Returns class as a JSON string.

        Args:
            None

        Returns:
            Class as a JSON: str
        """
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
            )


class Game(models.Model):
    """
    A class to represent a game.

    ...

    Attributes
    ----------
    name : str
        The tag name.
    slug : str
        The slug which is used in the url.
    tags: ManyToMany
        Links Game class with Tag class.
    image: Cloudinary
        Allows upload to Cloudinary hosting service.
    status: int
        Lets user pick from choices=STATUS.

    Methods
    -------
    __str__():
        returns name as the class str.

    to_json():
        converts class into a json string.
    """
    name = models.CharField(max_length=50, blank=False, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    tags = models.ManyToManyField(Tag, blank=False)
    image = CloudinaryField('image', null=True, default=None, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        """
        Returns name as the class str.

        Args:
            None

        Returns:
            name: str
        """
        return f"{self.name}"

    def to_json(self):
        """
        Returns class as a JSON string.

        Args:
            None

        Returns:
            Class as a JSON: str
        """
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
            )


class ServerListing(models.Model):
    """
    A class to represent a listing.

    ...

    Attributes
    ----------
    game : ForeignKey
        Links listing to a Game class.
    owner : ForeignKey
        Links listing to a CustomUser class.
    title: str
        The name of the listing.
    slug: str
        The slug which is used in the url.
    logo: CloudinaryField
        Allows upload to Cloudinary hosting service.
    tags: ManyToMany
        Links ServerListing class with Tag class.
    short_description: str
        A short introductory text field to introduce the listing.
    long_description: str
        A much longer description for users to view more detail about
        the listing.
    created_on: DateTime
        When the listing was created.
    updated_on: DateTime
        When the listing was last updated.
    discord: str
        The invite code used by Discord to invite new members.
        www.discord.com/?????????
    tiktok: str
        The profile link to share with users a listing TikTok page.
        www.tiktok.com/@???????
    status: int
        Lets user pick from choices=STATUS.
    bump_count: int
        Allows us to keep track of how many bumps the listing current has.

    Methods
    -------
    __str__():
        Returns title as the class str.

    bumpCount():
        Returns total amount of active bumps the listing has.
        Gets bump list from the Bumps class.

    number_of_tags():
        Returns total amount of tags currently linked to the listing.

    to_json():
        Converts class into a json string.

    save():
        Saves the object to the database.
        If new listing this method will assign a slug by getting the
        next available ID to use.
    """
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
        """
        Returns title as the class str.

        Args:
            None

        Returns:
            title: str
        """
        return self.title

    def bump_counter(self):
        """
        returns total amount of active bumps the listing has.
        Gets bump list from the Bumps class.

        Args:
            None

        Returns:
            bump count: int
        """
        return Bumps.objects.filter(listing=self.pk).count()

    def number_of_tags(self):
        """
        Returns total amount of tags currently linked to the listing.

        Args:
            None

        Returns:
            number of tags: int
        """
        return self.tags.count()

    def to_json(self):
        """
        Returns class as a JSON string.

        Args:
            None

        Returns:
            Class as a JSON: str
        """
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
            )

    def save(self, *args, **kwargs):
        """
        When saving object to database this method will check if it's a
        new entry. If so it will assign a new slug based on the next
        available ID.

        Args:
            None

        Returns:
            none
        """
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
    """
    A class to represent a Bump.

    ...

    Attributes
    ----------
    user : ForeignKey
        Links to a CustomUser class.
    listing : ForeignKey
        Links to a ServerListing class.
    date_added: Date
        Date bump was created.
    expiry: Date
        Date bump will expire, ready to be removed.

    Methods
    -------
    set_expiry():
        When bump is created, an expiry date is also applied.
    """

    @staticmethod
    def set_expiry():
        """
        Returns expiry date when bump is created.

        Decorator:
            @staticmethod

        Args:
            None

        Returns:
            expiry date: Date
        """
        return date.today() + timedelta(days=DAYS_TO_EXPIRE_BUMP)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    listing = models.ForeignKey(ServerListing, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    expiry = models.DateField(default=set_expiry(), blank=False)


class Images(models.Model):
    """
    A class to represent an Image.

    ...

    Attributes
    ----------
    image : Cloudinary
        Allows upload to Cloudinary hosting service.
    public_id : str
        Cloudinary image public id.
    user: ForeignKey
        The uploader. Links to a CustomUser class.
    reviewed_by: ForeignKey
        Which staff member reviewed the image. Links to a CustomUser class.
    listing: ForeignKey
        Links to a ServerListing class.
    status: int
        User can choose from 1 of 4 options. Unapproved, Approved, Rejected
        or 'Rejected and User banned'.
    date_added: Date
        Date image was uploaded to Cloudinary.
    expiry: Date: OPTIONAL
        If a date is present, the image will de deleted on this date.

    Methods
    -------
    None
    """

    image = CloudinaryField('image', default='placeholder')
    public_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_uploaded"
        )
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
