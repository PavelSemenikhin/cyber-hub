from django.contrib import admin
from django.utils.safestring import mark_safe
from tournaments.models import (
    Game,
    Tournament,
    TournamentApplication,
    TournamentParticipant
)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "cover_preview")
    search_fields = ("name",)
    readonly_fields = ("cover_preview",)

    def cover_preview(self, obj):
        if obj.cover:
            return mark_safe(
                f'<img src="{obj.cover.url}" width="100"'
                f' height="60" style="object-fit: cover;" />')
        return "(No image)"

    cover_preview.short_description = "Preview"


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
    search_fields = ("user__username",
                     "tournament__title",
                     "discord",
                     "telegram"
                     )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.status == "accepted":
            TournamentParticipant.objects.get_or_create(
                tournament=obj.tournament,
                user=obj.user
            )
