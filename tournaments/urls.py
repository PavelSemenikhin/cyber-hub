from django.urls import path

from tournaments.views import HomePageView, TournamentListView, TournamentDetailView

app_name = "tournaments"

#Роути для турнірів
urlpatterns = [
    #Роут на перегляд списку всіх турнірів
    path("", TournamentListView.as_view(), name="tournament-list"),
    #Роут на перегляд конкретного турніра
    path("<int:pk>/", TournamentDetailView.as_view(), name="tournament-detail"),
]
