from django.db import models

from django.conf import settings


#Моделі для турнірів

#Гра з якої цей турнір наприклад Dota2
class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

#Сам турнір який має гру, та власника, має статус дату початку та кінця, опис та призовий фонд, упорядковування по даті початку
class Tournament(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("finished", "Finished"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tournaments")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="tournaments")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class TournamentApplication(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    telegram = models.CharField(max_length=100)
    discord = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ("tournament", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} in {self.tournament.title}"
