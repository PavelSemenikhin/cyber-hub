from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from accounts.models import User, Profile
from tournaments.models import Game


#Форма реєстрації користувача + валідація username + email(необов`язковий)
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = False

    #Валідація username
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    #Валідація Email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


class ProfileUpdateForm(forms.ModelForm):
    favorite_games = forms.ModelMultipleChoiceField(
        queryset=Game.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = ("nickname", "favorite_games", "discord", "telegram", )
