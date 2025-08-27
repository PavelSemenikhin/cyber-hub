
from django.contrib import admin
from django.urls import path, include


from django.conf import settings
from tournaments.views import HomePageView


urlpatterns = [


    path("admin/", admin.site.urls),


    path("", HomePageView.as_view(), name="home"),


    path("tournaments/", include("tournaments.urls", namespace="tournaments")),


    path("accounts/", include("accounts.urls", namespace="accounts")),

    path("auth/", include("django.contrib.auth.urls")),


    path("blog/", include("blog.urls", namespace="blog")),
]
