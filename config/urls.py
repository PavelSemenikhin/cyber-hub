from django.contrib import admin
from django.urls import path, include

from tournaments.views import HomePageView

#Роут проекту
urlpatterns = [
    #Роут на адмін-панель
    path("admin/", admin.site.urls),
    #Роут на домашню сторінку
    path("", HomePageView.as_view(), name="home"),
    #Роут на сторінки турнірів
    path("tournaments/", include("tournaments.urls", namespace="tournaments")),
    #Роут на сторінки акаунтів
    path("accounts/", include("accounts.urls", namespace="accounts")),
    #Роут на сторінки блогу
    path("blog/", include("blog.urls", namespace="blog")),
]
