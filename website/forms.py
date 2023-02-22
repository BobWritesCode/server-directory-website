"""
All forms for website app
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm

from tinymce.widgets import TinyMCE

from cloudinary.forms import CloudinaryFileField

from .models import (
    CustomUser, Game, Tag, ServerListing, Images
)


class UserForm(forms.ModelForm):
    """
    A form to represent a user.
    Used to update user information.

    ...

    Meta
    ----------
    model: CustomUser

    Attributes
    ----------
    id : Integer
        Unique identity number for user.
    username : Char : REQUIRED
        Chosen by user to represent themselves.
    email : Char : REQUIRED
        User's primary email address.
    email_verified : Boolean : DISABLED
        Has use completed email verification.
    is_staff : Boolean : DISABLED
        Is the user a staff user.
    is_active : Boolean
        Can the user log in.
    is_banned : Boolean : DISABLED
        Has the account been banned.
    is_superuser : Boolean : DISABLED
        Is the user a superuser.

    Methods
    -------
    check_duplicates:
        checks to make sure no duplicate for username or email address.
        Raise an error if duplicates found.
    """
    id = forms.IntegerField(
        label="ID")
    username = forms.CharField(
        label="Username",
        max_length=20,
        required=True,
        strip=True)
    email = forms.EmailField(
        label="Email", required=True)
    email_verified = forms.BooleanField(
        label="Email verified?", disabled=True, required=False)
    is_staff = forms.BooleanField(
        label="Is Staff?", disabled=True, required=False)
    is_active = forms.BooleanField(
        label="Account Active?", required=False)
    is_banned = forms.BooleanField(
        label="Is Banned?", disabled=True, required=False)
    is_superuser = forms.BooleanField(
        label="Is Superuser?", disabled=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'email_verified',
            'is_active', 'is_banned', 'is_staff', 'is_superuser'
            ]


class ProfileForm(forms.ModelForm):
    """
    A form to represent a user.
    User for email updating.

    ...

    Meta
    ----------
    model: CustomUser

    Attributes
    ----------
    email : Email : REQUIRED
        User's primary email address.
    email_verified : Boolean : DISABLED
        Has use completed email verification.

    Methods
    -------
    none
    """
    email = forms.EmailField(
        label=("Email address"),
        required=True,
        error_messages={
            'required': "Email is required. (Falcon)", }
        )
    email_verified = forms.BooleanField(label=("Verified?"), disabled=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'email_verified']


class SignupForm(UserCreationForm):
    """
    A form to represent a user.
    User for user sign up.

    ...

    Meta
    ----------
    model: CustomUser

    Attributes
    ----------
    username : Char
        User's chosen username.
    email : Email
        User's primary email address.

    Methods
    -------
    __init__:
        Removed the default autofocus.
    """
    username = forms.CharField(
        label='Username', max_length=20,
        required=True,
        help_text='Required',
        error_messages={
            'required': 'Username is required. (Ferret)', })
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        required=True,
        error_messages={
            'required': 'Email is required. (Ferret)', })

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.pop('autofocus', None)


class ConfirmAccountDeleteForm(forms.ModelForm):
    """
    A form to represent a user.
    Used for account deletion.

    ...

    Meta
    ----------
    model: CustomUser

    Attributes
    ----------
    confirm : Char : REQUIRED
        Ask for user to type a specific phrase.

    Methods
    -------
    none
    """
    confirm = forms.CharField(
        label=(
            'To confirm deletion please type "remove" in the'
            'below box and then hit confirm:'),
        max_length=10,
        error_messages={'required': (
            'To confirm deletion please type "<strong>remove</strong>" '
            'in the below box and then hit confirm')},
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ['id']


class ConfirmServerListingDeleteForm(forms.ModelForm):
    """
    A form to represent a Listing.
    Used for listing deletion.

    ...

    Meta
    ----------
    model: ServerListing

    Attributes
    ----------
    server_listing_delete_confirm : Char : REQUIRED
        Ask for user to type a specific phrase.

    Methods
    -------
    none
    """
    server_listing_delete_confirm = forms.CharField(
        label=(
            'To confirm deletion please type "delete" '
            'in the below box and then hit confirm:'),
        max_length=10,
        error_messages={'required': (
            'To confirm deletion please type "<strong>delete</strong>" '
            'in the below box and then hit confirm')},
        required=True,
    )

    class Meta:
        model = ServerListing
        fields = ['id']


class ConfirmGameDeleteForm(forms.ModelForm):
    """
    A form to represent a Game.
    Used for game deletion.

    ...

    Meta
    ----------
    model: Game

    Attributes
    ----------
    game_delete_confirm : Char : REQUIRED
        Ask for user to type a specific phrase.

    Methods
    -------
    none
    """
    game_delete_confirm = forms.CharField(
        label=(
            'To confirm deletion please type "delete" in the '
            'below box and then hit confirm:'),
        max_length=10,
        error_messages={'required': (
            'To confirm deletion please type "<strong>delete</strong>" '
            'in the below box and then hit confirm')},
        required=True,
    )

    class Meta:
        model = Game
        fields = ['id']


class UserUpdateEmailAddressForm(forms.Form):
    """
    A form used for user email update.

    ...

    Meta
    ----------
    None

    Attributes
    ----------
    email : Email : REQUIRED
        Ask for user to type their email address.
    email_confirm : Email : REQUIRED
        Ask for user to retype their email address.

    Methods
    -------
    none
    """
    email = forms.EmailField(
        label='New email address:',
        error_messages={'required': 'Required'},
        required=True,
    )

    email_confirm = forms.EmailField(
        label='Repeat new email address:',
        error_messages={'required': 'Required'},
        required=True,
    )


class CreateServerListingForm(forms.ModelForm):
    """
    A form that allows the user to create a server listing.

    ...

    Meta
    ----------
    model : ServerListing

    Attributes
    ----------
    game : ModelChoice : REQUIRED
        Select game from the Game model class.
    tags : ModelMultipleChoice : REQUIRED
        Select multiple tags from the Tag model class.
    title : Char : REQUIRED
        User to provide name/title of server listing.
    short_description : Char : REQUIRED
        Provide a short description of the listing.
    long_description : Char : REQUIRED
        Provide a long description of the listing.
    status : TypedChoice : REQUIRED
        Choose to have listing as draft or published.
        (1, "Published"), (0, "Draft")
    discord : Char : REQUIRED
        Provide discord invite code.
        www.discord.com/?????????
    tiktok : Char
        Provide tiktok profile url.
        www.tiktok.com/@?????????

    Methods
    -------
    none
    """

    game = forms.ModelChoiceField(
        label="Choose game:",
        queryset=Game.objects.filter(status=1).order_by('name'),
        required=True,
        error_messages={'required': 'Choose a game.'},
    )

    tags = forms.ModelMultipleChoiceField(
        label="Choose tags:  (max: 10)",
        queryset=Tag.objects.order_by('name'),
        required=True,
        error_messages={
            'required': 'Choose at least 1 tag.'
        },
    )

    title = forms.CharField(
        label="Name of server:",
        max_length=50,
        required=True,
        error_messages={
            'required': 'Provide a server name.'
        },
    )

    short_description = forms.CharField(
        label="Short description: (min: 100, max: 200 characters)",
        min_length=100,
        max_length=200,
        widget=TinyMCE(attrs={'cols': 80, 'rows': 2}),
        required=True,
        error_messages={
            'required': 'Required.',
            'min_length': 'Must be over 100 and below 200 characters.',
            'max_length': 'Must be over 100 and below 200 characters.'
        },
    )

    long_description = forms.CharField(
        label="Long description: (min: 200, max: 2000 characters)",
        min_length=200,
        max_length=2000,
        widget=TinyMCE(attrs={'cols': 80, 'rows': 15, }),
        required=True,
        error_messages={
            'required': 'Required.',
            'min_length': 'Must be over 200 and below 2000 characters.',
            'max_length': 'Must be over 200 and below 2000 characters.'
        },
    )

    status = forms.TypedChoiceField(
        label="Status:",
        choices=((0, "Draft"), (1, "Published")),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial=0,
        required=True,
        error_messages={
            'required': 'Required.',
        },
    )

    discord = forms.CharField(
        label="Discord server invite:",
        max_length=10,
        required=True,
        error_messages={
            'required': 'Required.',
        },
    )

    tiktok = forms.CharField(
        label="Tiktok profile link:",
        max_length=20,
        required=False,
    )

    class Meta:
        model = ServerListing
        fields = [
            'game', 'tags', 'title', 'short_description',
            'long_description', 'status', 'discord', 'logo',
            'tiktok'
        ]


class ImageForm(forms.ModelForm):
    """
    A form that allows the user to choose image to upload.

    ...

    Meta
    ----------
    model : Images

    Attributes
    ----------
    image : Image
        Allow user to choose image to upload.

    Methods
    -------
    none
    """

    image = forms.ImageField(
        label="Upload image:",
        widget=forms.FileInput,
        required=False,
    )

    class Meta:
        model = Images
        fields = ['image']


class LoginForm(forms.ModelForm):
    """
    A form that allows the user to login.

    ...

    Meta
    ----------
    model : CustomUser

    Attributes
    ----------
    email : Email : REQUIRED
        User to provide email address.
    password : Char
        User to provide password.

    Methods
    -------
    none
    """

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class GameManageForm(forms.ModelForm):
    """
    A form used to update a Game.

    ...

    Meta
    ----------
    model : Game

    Attributes
    ----------
    id : Integer
        Unique number for each game.
    name : Char : REQUIRED
        Game title.
    slug : Slug
        Unique game url.
    tags : ModelMultipleChoice : REQUIRED
        Tags associated with Game.
        Tags provided by Tag class.
    Image : Cloudinary : REQUIRED
        Game image, uploaded to Cloudinary.
    Status : TypedChoice : REQUIRED
        User can choose from the following options,
        ((0, "Unpublish"), (1, "Publish")).


    Methods
    -------
    none
    """
    id = forms.IntegerField(required=False)
    name = forms.CharField(
        label="Game",
        max_length=50,
        required=True,
        error_messages={
            'required': 'Required.',
        },
        )
    slug = forms.SlugField(max_length=50)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        blank=False,
        error_messages={
            'required': 'Choose at least 1 tag.'
        },
    )
    image = CloudinaryFileField(
        label="Upload new image:",
        required=False,
    )
    status = forms.TypedChoiceField(
        label="Set status as:",
        choices=((0, "Draft"), (1, "Published")),
        initial=0,
        coerce=int,
        widget=forms.RadioSelect,
        required=True,
        error_messages={
            'required': 'Required.'
        },
    )

    class Meta:
        model = Game
        fields = ['id', 'name', 'slug', 'tags', 'image', 'status']


class TagsManageForm(forms.ModelForm):
    """
    A form used to update a Tag.

    ...

    Meta
    ----------
    model : Tag

    Attributes
    ----------
    id : Integer
        Unique number for each tag.
    name : Char : REQUIRED
        Tag title.
    slug : Slug
        Unique tag url.

    Methods
    -------
    none
    """
    id = forms.IntegerField(required=False)
    name = forms.CharField(
        label="Tag",
        max_length=50,
        required=True,
)
    slug = forms.SlugField(max_length=50)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class ConfirmTagDeleteForm(forms.ModelForm):
    """
    A form for user to confirm deletion a tag.

    ...

    Meta
    ----------
    model : Tag

    Attributes
    ----------
    tag_delete_confirm : Char : REQUIRED
        Ask for user to type a specific phrase.

    Methods
    -------
    none
    """
    tag_delete_confirm = forms.CharField(
        label=(
            'To confirm deletion please type "delete" in '
            'the below box and then hit confirm:'),
        max_length=10,
        required=True,
        error_messages={'required': 'Follow the instructions.'},
    )

    class Meta:
        model = Tag
        fields = ['id']


class DeleteConfirmForm(forms.Form):
    """
    A form for general deletion confirmation.

    ...

    Meta
    ----------
    None

    Attributes
    ----------
    tag_delete_confirm : Char : REQUIRED
        Ask for user to type a specific phrase.

    Methods
    -------
    none
    """
    delete_confirm = forms.CharField(
        label=(
            'To confirm deletion please type "delete" '
            'in the below box and then hit confirm:'),
        max_length=10,
        error_messages={'required': 'Follow the instructions.'},
        required=True,
    )
