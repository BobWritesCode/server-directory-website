from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    '''
    A form that allows the user to update their profile information.
    '''
    email = forms.EmailField(label = ("Email address"), required = True)

    class Meta:
        model = User
        fields = ['email']


