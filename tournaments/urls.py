from django.urls import path

from tournaments.views import (
    TournamentListView,
    TournamentDetailView,
    apply_to_tournament
)

app_name = "tournaments"

urlpatterns = [
    path("", TournamentListView.as_view(), name="tournament-list"),
    path(
        "<int:pk>/",
        TournamentDetailView.as_view(),
        name="tournament-detail"
    ),
    path("<int:pk>/apply/", apply_to_tournament, name="apply"),
]
