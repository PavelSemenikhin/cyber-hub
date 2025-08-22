from django.urls import path

from accounts.views import AccountsView

app_name = "accounts"

#Роути для акаунтів
urlpatterns = [
    path("login/", AccountsView.as_view(), name="accounts"),
]

