from django.urls import path, include

from accounts.views import RegisterView, ProfileView, ProfileUpdateView

app_name = "accounts"

#Роути для акаунтів
urlpatterns = [

    #Реєстрація
    path("register/", RegisterView.as_view(), name="register"),

    #Профіль користувача
    path("profile/", ProfileView.as_view(), name="profile"),

    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),

]
