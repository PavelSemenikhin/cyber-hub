from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from tournaments.models import Tournament, TournamentApplication
from tournaments.forms import TournamentApplicationForm


#Вью турнірів
class HomePageView(ListView):
    model = Tournament
    template_name = "tournaments/home.html"
    context_object_name = "tournaments"


#Вью сторінки всіх турнірів
class TournamentListView(ListView):
    model = Tournament
    template_name = "tournaments/tournaments_list.html"
    context_object_name = "tournaments"

    def get_queryset(self):
        status = self.request.GET.get("status")
        if status in ["registration", "in_progress"]:
            return Tournament.objects.filter(status=status)
        return Tournament.objects.filter(status__in=["registration", "in_progress"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status", "all")
        return context


#Вью перегляду турніру
class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "tournaments/tournament_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()
        if self.request.user.is_authenticated:
            context["has_applied"] = tournament.applications.filter(user=self.request.user).exists()
        return context


@login_required
def apply_to_tournament(request: HttpRequest, pk: int) -> HttpResponse:
    tournament = get_object_or_404(Tournament, pk=pk)

    if tournament.status != "registration":
        messages.error(request, "Registration is closed.")
        return redirect("tournaments:tournament-detail", pk=pk)

    if TournamentApplication.objects.filter(tournament=tournament, user=request.user).exists():
        messages.warning(request, "You have already applied.")
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
        {"form": form, "tournament": tournament}
    )