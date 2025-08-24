from django.contrib import admin
from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "created_at", "updated_at", "is_published",)
    search_fields = ("title", "body", "owner__username",)
    list_filter = ("is_published", "created_at", "updated_at",)
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "owner", "created_at",)
    search_fields = ("body", "owner__username", "post__title",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)
