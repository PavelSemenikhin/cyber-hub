from django import forms

from tournaments.models import TournamentApplication


class TournamentApplicationForm(forms.ModelForm):
    class Meta:
        model = TournamentApplication
        fields = ["telegram", "discord", "about"]
        widgets = {
            "about": forms.Textarea(attrs={"rows": 3}),
        }
