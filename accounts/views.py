from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, UpdateView
from django.contrib import messages

from accounts.forms import RegisterForm, ProfileUpdateForm
from accounts.models import User, Profile
from blog.models import Post
from tournaments.models import TournamentApplication


# Реєстрація нового користувача з автологіном
class RegisterView(generic.CreateView):
    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


# Відображення профілю користувача
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = self.request.user
            context["profile"] = user.profile
            context["posts"] = Post.objects.filter(owner=user).order_by("-created_at")

            # Отримання поточного турніру, якщо є прийнята заявка
            application = TournamentApplication.objects.filter(user=user, status="accepted").select_related("tournament").first()
            if application:
                context["current_tournament"] = application.tournament

        except Profile.DoesNotExist:
            messages.error(self.request, "Ваш профіль ще не створено.")
            return redirect("home")

        return context


# Редагування профілю
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
