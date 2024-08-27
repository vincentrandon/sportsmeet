from django.contrib import admin

from planner.models import Championship, Match, Player, Team, Attendance, SubChampionship


# Register your models here.
@admin.register(Championship)
class ChampionshipAdmin(admin.ModelAdmin):
    pass


@admin.register(SubChampionship)
class SubChampionshipAdmin(admin.ModelAdmin):
    pass

@admin.register(Match)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass
