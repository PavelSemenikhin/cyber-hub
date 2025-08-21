from django.db import models
from django.conf import settings

# Моделі для блогу

#Пост користувача
class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)


    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_published"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title


#Коментарі до поста
class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["is_deleted"]),
        ]

    def __str__(self):
        return f"Comment by {self.owner.username} on {self.post.title}"
