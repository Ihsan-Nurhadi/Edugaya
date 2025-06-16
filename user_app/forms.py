from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from learning_style.models import Student

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    profile_pic = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control-file"
            }
        ),
        required=False  # Optional profile picture
    )


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'profile_pic')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name']  # Hanya mengambil field name saja
        widgets = {
            'name': forms.TextInput(attrs={"class":"form-control"})
        }

