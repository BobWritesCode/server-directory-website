from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML

from website.models import Game, Tag, ServerListing


class ProfileForm(forms.ModelForm):
    '''
    A form that allows the user to update their profile information.
    '''
    email = forms.EmailField(label=("Email address"), required=True)

    class Meta:
        model = User
        fields = ['email']

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
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
        model = User
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

    logo = forms.ImageField(
        label="Update image:",
        widget=forms.FileInput,
        required=False,
    )

    class Meta:
        model = ServerListing
        fields = ['game', 'tags', 'title', 'short_description',
                  'long_description', 'status', 'discord', 'logo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'first arg is the legend of the fieldset',
                'game',
                'title',
                HTML(
                    """{% if item.logo.url %}<img class="img-fluid" src="{{ item.logo.url }}">{% endif %}""", ),
                'logo',
                'tags',
                'short_description',
                'long_description',
                'discord',
                'status',
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )
