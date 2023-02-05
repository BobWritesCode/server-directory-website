from django import forms
from django.contrib.auth.forms import UserCreationForm

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
    email = forms.EmailField(label=("Email address"), required=True, disabled=True)
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
        label="Choose tags:",
        queryset=Tag.objects.order_by('name'),
        required=True,
    )

    title = forms.CharField(
        label="Name of server:",
        max_length=50,
        required=True,
    )

    short_description = forms.CharField(
        label="Short description:",
        max_length=200,
        widget=forms.Textarea,
        required=True,
    )

    long_description = forms.CharField(
        label="Long description:",
        max_length=2000,
        widget=forms.Textarea,
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
    id = forms.IntegerField(disabled=True)
    name = forms.CharField(label="Game", max_length=50, required=True)
    slug = forms.SlugField(max_length=50, disabled=True)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), blank=False)
    image = forms.ImageField(
        label="Upload image:",
        widget=forms.FileInput,
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
                'tags,'
                'image',
                InlineRadios('status')
            ),
            Submit('submit', 'Submit', css_class='button white'),
        )