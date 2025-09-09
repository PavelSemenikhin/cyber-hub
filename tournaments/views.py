from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from tournaments.models import (
    Tournament,
    TournamentApplication,
    TournamentStatus,
    ApplicationStatus,
)
from tournaments.forms import TournamentApplicationForm


class HomePageView(ListView):
    model = Tournament
    template_name = "tournaments/home.html"
    context_object_name = "tournaments"


class TournamentsListView(ListView):
    model = Tournament
    template_name = "tournaments/tournaments_list.html"
    context_object_name = "tournaments"

    def get_queryset(self):
        status = self.request.GET.get("status")
        queryset = (
            super().get_queryset()
            .select_related("game", "owner")
            .prefetch_related("participants", "applications")
            .order_by("-created_at")
        )
        if status:
            queryset = queryset.filter(status=status)

        for tournament in queryset:
            tournament.update_status()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status", "")

        if self.request.user.is_authenticated:
            user_applications = TournamentApplication.objects.filter(
                user=self.request.user
            )
            applied_ids = set(
                user_applications.values_list("tournament_id", flat=True)
            )
            context["applied_tournaments"] = applied_ids
        else:
            context["applied_tournaments"] = set()

        return context


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "tournaments/tournament_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.object
        if self.request.user.is_authenticated:
            context["has_applied"] = tournament.applications.filter(
                user=self.request.user
            ).exists()
        return context


@login_required
def apply_to_tournament(request: HttpRequest, pk: int) -> HttpResponse:
    tournament = get_object_or_404(Tournament, pk=pk)

    if tournament.status != TournamentStatus.REGISTRATION:
        messages.error(request, "Registration is closed.")
        return redirect("tournaments:tournament-detail", pk=pk)

    if TournamentApplication.objects.filter(
        user=request.user,
        status__in=[ApplicationStatus.PENDING, ApplicationStatus.ACCEPTED],
    ).exclude(tournament=tournament).exists():
        messages.warning(request, "You already applied to another tournament.")
        return redirect("tournaments:tournament-detail", pk=pk)

    if TournamentApplication.objects.filter(
        tournament=tournament, user=request.user
    ).exists():
        messages.warning(request, "You have already applied.")
        return redirect("tournaments:tournament-detail", pk=pk)

    if tournament.participants.count() >= 2:
        messages.error(request, "Tournament already has 2 participants.")
        return redirect("tournaments:tournament-detail", pk=pk)

    if request.method == "POST":
        form = TournamentApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.tournament = tournament
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect("tournaments:tournament-detail", pk=pk)
    else:
        form = TournamentApplicationForm()

    return render(
        request,
        "tournaments/apply.html",
        {"form": form, "tournament": tournament},
    )
