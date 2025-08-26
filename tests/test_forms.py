import pytest
from accounts.forms import RegisterForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from accounts.models import Profile
from tournaments.models import Game


User = get_user_model()


@pytest.mark.django_db
def test_register_form_valid():
    form = RegisterForm(data={
        "username": "testuser",
        "email": "test@example.com",
        "password1": "Testpass123!",
        "password2": "Testpass123!",
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_register_form_duplicate_username():
    User.objects.create_user(username="testuser", password="pass")
    form = RegisterForm(data={
        "username": "testuser",
        "email": "other@example.com",
        "password1": "pass12345",
        "password2": "pass12345",
    })
    assert not form.is_valid()
    assert "username" in form.errors