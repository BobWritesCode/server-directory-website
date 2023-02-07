from django import forms
from django.contrib.auth.forms import UserCreationForm

from tinymce.widgets import TinyMCE

from cloudinary.forms import CloudinaryFileField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from crispy_forms.bootstrap import InlineRadios, Field

from .constants import STATUS
from .models import (
    CustomUser, Game, Tag, ServerListing, Images
)


class ProfileForm(forms.ModelForm):
    '''
    A form that allows the user to update their profile information.
    '''
    email = forms.EmailField(label=("Email address"), required=True)
    email_verified = forms.BooleanField(label=("Verified?"), disabled=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'email_verified']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class ConfirmAccountDeleteForm(forms.ModelForm):
    '''
    A form for user to confirm deletion of their account.
    '''
    confirm = forms.CharField(
        label=f'To confirm deletion please type "remove" in the below box and then hit confirm:',
        max_length=10,
        error_messages={
            'required': f'To confirm deletion please type "<strong>remove</strong>" in the below box and then hit confirm'},
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ['id']


class ConfirmServerListingDeleteForm(forms.ModelForm):
    '''
    A form for user to confirm deletion a server listing.
    '''
    server_listing_delete_confirm = forms.CharField(
        label=f'To confirm deletion please type "delete" in the below box and then hit confirm:',
        max_length=10,
        error_messages={
            'required': f'To confirm deletion please type "<strong>delete</strong>" in the below box and then hit confirm'},
        required=True,
    )

    class Meta:
        model = ServerListing
        fields = ['id']


class ConfirmGameDeleteForm(forms.ModelForm):
    '''
    A form for user to confirm deletion a game.
    '''
    game_delete_confirm = forms.CharField(
        label=f'To confirm deletion please type "delete" in the below box and then hit confirm:',
        max_length=10,
        error_messages={
            'required': f'To confirm deletion please type "<strong>delete</strong>" in the below box and then hit confirm'},
        required=True,
    )

    class Meta:
        model = Game
        fields = ['id']


class UserUpdateEmailAddressForm(forms.ModelForm):
    '''
    A form for user to update their email address.
    '''
    email = forms.EmailField(
        label=f'New email address:',
        error_messages={'required': f'Required'},
        required=True,
    )

    email_confirm = forms.EmailField(
        label=f'Repeat new email address:',
        error_messages={'required': f'Required'},
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ['id']


class CreateServerListingForm(forms.ModelForm):
    '''
    A form that allows the user to create a server listing.
    '''

    game = forms.ModelChoiceField(
        label="Choose game:",
        queryset=Game.objects.filter(status=1).order_by('name'),
        required=True,
    )

    tags = forms.ModelMultipleChoiceField(
        label="Choose tags:  (max: 10)",
        queryset=Tag.objects.order_by('name'),
        required=True,
    )

    title = forms.CharField(
        label="Name of server:",
        max_length=50,
        required=True,
    )

    short_description = forms.CharField(
        label="Short description: (min: 100, max: 200 characters)",
        min_length=100,
        max_length=200,
        widget=TinyMCE(attrs={'cols': 80, 'rows': 2}),
        required=True,
    )

    long_description = forms.CharField(
        label="Long description: (min: 200, max: 2000 characters)",
        min_length=200,
        max_length=2000,
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30, }),
        required=True,
    )

    status = forms.TypedChoiceField(
        label="Status:",
        choices=((1, "Published"), (0, "Draft")),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial='0',
        required=True,
    )

    discord = forms.CharField(
        label="Discord server invite:",
        max_length=10,
        required=True,
    )

    class Meta:
        model = ServerListing
        fields = [
            'game', 'tags', 'title', 'short_description',
            'long_description', 'status', 'discord', 'logo'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '', # First arg is the legend of the fieldset
                'game',
                'title',
                HTML(
                    """{% if item.logo.url %}<img class="img-fluid" src="{{ item.logo.url }}">{% endif %}""", ),
                'tags',
                'short_description',
                'long_description',
                'discord',
                'status',
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )

class ImageForm(forms.ModelForm):

    image = forms.ImageField(
        label="Upload image:",
        widget=forms.FileInput,
        required=False,
    )

    class Meta:
        model = Images
        fields = ['image']


class LoginForm(forms.ModelForm):

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class GameListForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Game
        fields = ['name']

class GameManageForm(forms.ModelForm):
    id = forms.IntegerField()
    name = forms.CharField(label="Game", max_length=50, required=True)
    slug = forms.SlugField(max_length=50)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), blank=False)
    image = CloudinaryFileField(
        label="Upload new image:",
        required=False,
    )
    status = forms.TypedChoiceField(
        label="Set status as:",
        choices=((0, "Unpublish"), (1, "Publish")),
        coerce=lambda x: int(x),
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = Game
        fields = ['id', 'name', 'slug', 'tags', 'image', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'id',
                'name',
                'slug',
                'tags',
                'image',
                InlineRadios('status')
            ),
            Submit('submit', 'Submit', css_class='button white'),
        )

class TagsManageForm(forms.ModelForm):
    id = forms.IntegerField()
    name = forms.CharField(label="Tag", max_length=50, required=True)
    slug = forms.SlugField(max_length=50)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'id',
                'name',
                'slug',
            ),
            Submit('submit', 'Submit', css_class='button white'),
        )


class ConfirmTagDeleteForm(forms.ModelForm):
    '''
    A form for user to confirm deletion a tag.
    '''
    tag_delete_confirm = forms.CharField(
        label=f'To confirm deletion please type "delete" in the below box and then hit confirm:',
        max_length=10,
        error_messages={
            'required': f'To confirm deletion please type "<strong>delete</strong>" in the below box and then hit confirm'},
        required=True,
    )

    class Meta:
        model = Tag
        fields = ['id']
