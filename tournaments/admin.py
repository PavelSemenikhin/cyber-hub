from django.contrib import admin

from tournaments.models import Game, Tournament, TournamentApplication


# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "title",
        "description",
        "game",
        "status",
        "start_at",
        "end_at",
        "prize_pool",
        "created_at",
    )
    search_fields = ("owner__username", "game__name", "title", "description",)
    list_filter = ("status", "game", "start_at",)


@admin.register(TournamentApplication)
class TournamentApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "tournament",
        "user",
        "telegram",
        "discord",
        "about",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "tournament__title", "discord", "telegram")