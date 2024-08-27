from django.conf.urls.static import static
from django.urls import path

from config import settings
from planner.views import index, single_match, team_index, create_team, search_players, add_player, edit_team, \
    nominate_captain, matches_index, create_match, select_players, delete_team, delete_match, edit_match_team, \
    send_confirmation_email, confirm_attendance, search, load_subchampionships, create_championship, \
    create_subchampionship, confirm_attendance_manual, remove_attendance

app_name = 'planner'
urlpatterns = [
    path('', index, name='index'),

    #championships

    #matches
    path('matches/', matches_index, name='matches-index'),
    path('matches/<str:slug>', single_match, name='match-detail'),
    path('matches/create/', create_match, name='create-match'),
    path('matches/<int:match_id>/select-players/', select_players, name='select-players'),
    path('matches/<str:slug>/delete/', delete_match, name='delete-match'),
    path('matches/<str:slug>/edit-team/', edit_match_team, name='edit-match-team'),

    #teams
    path('teams/', team_index, name='team-index'),
    path('teams/create/', create_team, name='team-create'),
    path('teams/search-players/', search_players, name='search-players'),
    path('teams/add-player/', add_player, name='add-player'),
    path('teams/nominate-captain/', nominate_captain, name='nominate-captain'),
    path('teams/<int:team_id>/edit/', edit_team, name='team-edit'),
    path('teams/<int:team_id>/delete/', delete_team, name='team-delete'),
    path('teams/load-subchampionships/', load_subchampionships, name='load-subchampionships'),
    path('teams/create/create-championship/', create_championship, name='create-championship'),
    path('teams/create/create-subchampionship/', create_subchampionship, name='create-subchampionship'),

    #attendances
    path('send-confirmation-email/<int:attendance_id>/', send_confirmation_email, name='send_confirmation_email'),
    path('confirm-attendance/<str:token>/', confirm_attendance, name='confirm_attendance'),
    path('confirm-attendance-manual/<int:attendance_id>/', confirm_attendance_manual, name='confirm_attendance_manual'),
    path('remove-attendance/<int:attendance_id>/', remove_attendance, name='remove_attendance'),



    #search
    path('search/', search, name='search'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
