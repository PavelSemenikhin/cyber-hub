from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, DetailView

from tournaments.models import Tournament

#Вью турнірів

class HomePageView(ListView):
    model = Tournament
    template_name = "tournaments/home.html"
    context_object_name = "tournaments"


    def get_queryset(self):
        return Tournament.objects.filter(status="active").order_by("-created_at")[:5]


class TournamentListView(ListView):
    model = Tournament
    template_name = "tournaments/tournaments_list.html"
    context_object_name = "tournaments"

    def get_queryset(self):
        return Tournament.objects.order_by("-created_at")


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "tournaments/tournament_detail.html"