from django import forms
from django.contrib.auth.models import User
from website.models import Game, Tag, ServerListing


class ProfileForm(forms.ModelForm):
    '''
    A form that allows the user to update their profile information.
    '''
    email = forms.EmailField(label = ("Email address"), required = True)

    class Meta:
        model = User
        fields = ['email']


class CreateServerListingForm(forms.ModelForm):
    '''
    A form that allows the user to create a server listing.
    '''
    game = forms.ModelChoiceField(queryset=Game.objects.filter(status=1).order_by('name'))
    tags = forms.ModelMultipleChoiceField(Tag.objects)
    title = forms.CharField(max_length=50)
    short_description = forms.CharField(max_length=200, widget=forms.Textarea)
    long_description = forms.CharField(max_length=2000, widget=forms.Textarea)
    status = forms.ChoiceField(choices=((0, 'Draft'),(1, 'Published')))
    discord =  forms.CharField(max_length=50)

    class Meta:
        model = ServerListing
        fields = ['game', 'tags', 'title', 'short_description', 'long_description', 'status', 'discord']
