from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,UserProfile

from RestroBook .models import Booking

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    class Meta:
        model = User
        fields = ['username','email','password1','password2','role']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']