from django.urls import path

from accounts.views import RegisterView, ProfileView, ProfileUpdateView

app_name = "accounts"

urlpatterns = [

    path("register/", RegisterView.as_view(), name="register"),

    path("profile/", ProfileView.as_view(), name="profile"),

    path(
        "profile/update/",
        ProfileUpdateView.as_view(),
        name="profile-update"
    ),

]
