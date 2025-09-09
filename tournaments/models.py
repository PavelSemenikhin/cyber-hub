from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TournamentStatus(models.TextChoices):
    REGISTRATION = "registration", "Registration"
    IN_PROGRESS = "in_progress", "In progress"
    FINISHED = "finished", "Finished"


class Tournament(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tournaments"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="tournaments"
    )
    status = models.CharField(
        max_length=20,
        choices=TournamentStatus.choices,
        default=TournamentStatus.REGISTRATION,
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(blank=True, null=True)
    prize_pool = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def is_registration_open(self):
        return self.status == TournamentStatus.REGISTRATION

    def update_status(self):
        current_time = now()

        if self.end_at and current_time > self.end_at:
            new_status = TournamentStatus.FINISHED
        elif self.start_at and current_time >= self.start_at:
            new_status = TournamentStatus.IN_PROGRESS
        else:
            new_status = TournamentStatus.REGISTRATION

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=["status"])


class ApplicationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class TournamentApplication(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    telegram = models.CharField(max_length=100)
    discord = models.CharField(max_length=100)
    about = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["tournament", "user"],
                name="unique_application"
            )
        ]

    def __str__(self):
        return f"{self.user.username} in {self.tournament.title}"


class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="participants"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tournament_participations"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tournament", "user"],
                name="unique_participant"
            )
        ]

    def __str__(self):
        return f"{self.user.username} — participant of {self.tournament.title}"
