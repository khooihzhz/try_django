from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Photo
from captcha.fields import ReCaptchaField


# this creates a user form with email address
class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail : ")
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Username : "
        self.fields['email'].label = "E-mail : "
        self.fields['password1'].label = "Password : "
        self.fields['password2'].label = "Re-enter Password : "
        self.fields['captcha'].required = True

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CaptchaAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(CaptchaAuthenticationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'password1')


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('name', 'photo')

