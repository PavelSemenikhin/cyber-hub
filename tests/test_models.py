import pytest
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from accounts.models import Profile
from blog.models import Post, Comment
from tournaments.models import (
    Game,
    Tournament,
    TournamentApplication,
    TournamentParticipant
)


User = get_user_model()


@pytest.mark.django_db
def test_user_and_profile_str():
    user = User.objects.create_user(username="testuser", password="pass")
    profile = user.profile
    profile.nickname = "ProPlayer"
    profile.save()
    assert str(profile) == "ProPlayer"

    profile.nickname = ""
    profile.save()
    assert str(profile) == "testuser"


@pytest.mark.django_db
def test_profile_favorite_games():
    user = User.objects.create_user(username="gamer", password="pass")
    game1 = Game.objects.create(name="Dota 2")
    game2 = Game.objects.create(name="CS2")
    profile = user.profile
    profile.favorite_games.set([game1, game2])
    assert list(profile.favorite_games.all()) == [game1, game2]


@pytest.mark.django_db
def test_post_and_comment_models():
    user = User.objects.create_user(username="author", password="pass")
    game = Game.objects.create(name="Valorant")
    post = Post.objects.create(title="Test Post", body="Content", owner=user, game=game)

    assert str(post) == "Test Post"
    assert post.game == game

    comment = Comment.objects.create(post=post, owner=user, body="Nice post!")
    assert str(comment) == f"Comment by {user.username} on {post.title}"


@pytest.mark.django_db
def test_game_model_str():
    game = Game.objects.create(name="PUBG")
    assert str(game) == "PUBG"


@pytest.mark.django_db
def test_tournament_and_related_models():
    user = User.objects.create_user(username="player", password="pass")
    game = Game.objects.create(name="Fortnite")

    tournament = Tournament.objects.create(
        title="Fortnite Cup",
        description="A battle royale tournament",
        start_at=timezone.now() + timedelta(days=5),
        end_at=timezone.now() + timedelta(days=10),
        game=game,
        owner=user,
        prize_pool=1000.00,
        status="registration"
    )
    assert str(tournament) == "Fortnite Cup (Registration)"
    assert tournament.is_registration_open()

    app = TournamentApplication.objects.create(
        user=user,
        tournament=tournament,
        telegram="@player",
        discord="player#1234",
        about="I am ready!"
    )
    assert str(app) == f"{user.username} in {tournament.title}"

    participant = TournamentParticipant.objects.create(
        user=user,
        tournament=tournament
    )
    assert str(participant) == f"{user.username} — participant of {tournament.title}"


@pytest.mark.django_db
def test_tournament_application_unique_constraint():
    user = User.objects.create_user(username="uniqueuser", password="pass")
    game = Game.objects.create(name="CS2")
    tournament = Tournament.objects.create(
        title="1v1 Challenge",
        description="Single match",
        start_at=timezone.now(),
        game=game,
        owner=user
    )
    TournamentApplication.objects.create(
        user=user,
        tournament=tournament,
        telegram="@user",
        discord="user#0001"
    )

    with pytest.raises(Exception):
        TournamentApplication.objects.create(
            user=user,
            tournament=tournament,
            telegram="@user2",
            discord="user#0002"
        )
