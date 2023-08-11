from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_photo = forms.ImageField(required=False)  # Add the profile_photo field

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'bio', 'profile_photo')




class CustomUserInforForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'status', 'bio']
