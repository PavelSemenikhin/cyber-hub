import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Profile
from blog.models import Post, Comment
from tournaments.models import Game, Tournament, TournamentApplication

User = get_user_model()


@pytest.mark.django_db
def test_blog_list_view(client):
    response = client.get(reverse("blog:blog"))
    assert response.status_code == 200
    assert "posts" in response.context


@pytest.mark.django_db
def test_post_detail_view(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    game = Game.objects.create(name="Test Game")
    post = Post.objects.create(owner=user, title="Test", body="Body", game=game)
    url = reverse("blog:post-detail", kwargs={"pk": post.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["post"] == post


@pytest.mark.django_db
def test_post_detail_comment_submission(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    game = Game.objects.create(name="Test Game")
    post = Post.objects.create(owner=user, title="Test", body="Body", game=game)
    client.force_login(user)
    url = reverse("blog:post-detail", kwargs={"pk": post.pk})
    data = {"body": "Great post!"}
    response = client.post(url, data)
    assert response.status_code == 200
    assert Comment.objects.filter(post=post, body="Great post!").exists()


@pytest.mark.django_db
def test_post_create_view(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.force_login(user)
    game = Game.objects.create(name="Test Game")
    url = reverse("blog:post-create")
    data = {"title": "New Post", "body": "Some content", "game": game.pk}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Post.objects.filter(title="New Post").exists()


@pytest.mark.django_db
def test_post_update_view(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    game = Game.objects.create(name="Test Game")
    post = Post.objects.create(owner=user, title="Original", body="Body", game=game)
    client.force_login(user)
    url = reverse("blog:post-update", kwargs={"pk": post.pk})
    data = {"title": "Updated", "body": "Updated content", "game": game.pk}
    response = client.post(url, data)
    assert response.status_code == 302
    post.refresh_from_db()
    assert post.title == "Updated"


@pytest.mark.django_db
def test_post_delete_view(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    post = Post.objects.create(owner=user, title="Delete Me", body="x")
    client.force_login(user)
    url = reverse("blog:post-delete", kwargs={"pk": post.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert not Post.objects.filter(pk=post.pk).exists()


@pytest.mark.django_db
def test_comment_delete_view(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    post = Post.objects.create(owner=user, title="Test", body="Body")
    comment = Comment.objects.create(owner=user, post=post, body="Comment")
    client.force_login(user)
    url = reverse("blog:comment-delete", kwargs={"pk": comment.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert not Comment.objects.filter(pk=comment.pk).exists()
