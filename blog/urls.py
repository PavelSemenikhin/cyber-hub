from django.urls import path

from blog.views import BlogListView

app_name = "blog"

#Роути для блогів
urlpatterns = [
    path("", BlogListView.as_view(), name="blog"),
]

