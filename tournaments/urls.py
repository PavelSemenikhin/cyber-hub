from django.urls import path

from tournaments.views import (
    TournamentsListView,
    TournamentDetailView,
    apply_to_tournament
)

app_name = "tournaments"

urlpatterns = [
    path("", TournamentsListView.as_view(), name="tournaments_list"),
    path(
        "<int:pk>/",
        TournamentDetailView.as_view(),
        name="tournament_detail"
    ),
    path("<int:pk>/apply/", apply_to_tournament, name="apply"),
]
