from django import forms
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("user",)


class SignUpForm(UserCreationForm):

    CUSTOMER = 'customer'
    VENDOR = 'vendor'
    USER_TYPE_CHOICES = [
        (CUSTOMER, 'I am a customer'),
        (VENDOR, 'I am a vendor'),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True, label="", initial=CUSTOMER
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2", "user_type")
