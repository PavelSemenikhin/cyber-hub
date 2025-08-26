from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings
from tournaments.views import HomePageView


urlpatterns = [


    path("admin/", admin.site.urls),


    path("", HomePageView.as_view(), name="home"),


    path("tournaments/", include("tournaments.urls", namespace="tournaments")),


    path("accounts/", include("accounts.urls", namespace="accounts")),

    path("auth/", include("django.contrib.auth.urls")),


    path("blog/", include("blog.urls", namespace="blog")),
]

# Вимкнути під час деплою
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
