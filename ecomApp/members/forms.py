from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        widgets = {
            "email": forms.TextInput(attrs={'placeholder': "Enter your email address", 'class': 'form-control'}),
            "username": forms.TextInput(attrs={'placeholder': "Enter your username", 'class': 'form-control'}),
            'password': forms.TextInput(attrs={'placeholder': "Enter password", 'class': 'form-control', "type": "password"})
        }
        labels= {
            "email": ("Email of user"), 
            "username": ("Username"), 
            "Password": ("Password"), 
        }
        help_texts = {
            "username": ("")
        }
