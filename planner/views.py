import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import UpdateView

from config import settings
from planner.forms import TeamCreateForm, MatchForm, ChampionshipForm, SubChampionshipForm
from planner.models import Championship, Match, Player, Team, Attendance, SubChampionship
from planner.utils import generate_token, validate_token


@login_required
def index(request):
    upcoming_matches = Match.objects.filter(date__gte=timezone.now()).order_by('date')
    past_matches = Match.objects.filter(date__lt=timezone.now()).order_by('-date')

    # Annotate matches with confirmed attendance count
    upcoming_matches = upcoming_matches.annotate(
        confirmed_count=Count('attendance', filter=Q(attendance__present=True))
    )

    # Paginate upcoming matches
    paginator = Paginator(upcoming_matches, 10)  # Show 10 matches per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'upcoming_matches': page_obj,
        'past_matches': past_matches,
    }

    if request.htmx:
        return render(request, 'home/partials/upcoming-matches.html', context)
    return render(request, 'home/index.html', context)

# CHAMPIONSHIPS

@login_required
def create_championship(request):
    if request.method == 'POST':
        form = ChampionshipForm(request.POST)
        if form.is_valid():
            championship = form.save()
            return JsonResponse({
                'success': True,
                'option': f'<option value="{championship.id}" selected>{championship.name}</option>',
                'toast': {
                    'title': 'Success!',
                    'message': 'A new championship has been created.'
                }
            })
    else:
        form = ChampionshipForm()
    return render(request, 'championships/championship-form.html', {'form': form})


@login_required
def create_subchampionship(request):
    if request.method == 'POST':
        form = SubChampionshipForm(request.POST)
        if form.is_valid():
            subchampionship = form.save()
            return JsonResponse({
                'success': True,
                'option': f'<option value="{subchampionship.id}" selected>{subchampionship.name}</option>',
                'toast': {
                    'title': 'Success!',
                    'message': 'A new subchampionship has been created.'
                }
            })
    else:
        form = SubChampionshipForm()
    return render(request, 'championships/subchampionship-form.html', {'form': form})


### MATCHES


@login_required
def matches_index(request):
    # Get all matches
    matches = Match.objects.all().order_by('-date')

    # Filter by championship
    championship_id = request.GET.get('championship')
    if championship_id:
        matches = matches.filter(championship_id=championship_id)

    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        matches = matches.filter(date__range=[start_date, end_date])

    # Search
    search_query = request.GET.get('search')
    if search_query:
        matches = matches.filter(
            Q(team1__name__icontains=search_query) |
            Q(team2__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(matches, 10)  # Show 10 matches per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Get all championships for the filter dropdown
    championships = Championship.objects.all()

    context = {
        'page_obj': page_obj,
        'championships': championships,
        'current_page': int(page_number)
    }

    if request.htmx:
        return render(request, 'matches/partials/matches-table-body.html', context)
    return render(request, 'matches/matches.html', context)

@login_required
def single_match(request, slug):
    match = get_object_or_404(Match, slug=slug)
    team = match.team1
    all_players = team.players.all()
    attendances = Attendance.objects.filter(match=match)

    context = {
        'match': match,
        'all_players': all_players,
        'attendances': attendances,
        'selected_count': attendances.count()
    }
    return render(request, 'matches/single-match.html', context)

@login_required
def create_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save()
            return redirect('planner:select-players', match_id=match.id)
    else:
        form = MatchForm()

    return render(request, 'matches/create-match.html', {'form': form})

@login_required
def edit_match_team(request, slug):
    match = get_object_or_404(Match, slug=slug)
    team = match.team1
    all_players = team.players.all()
    current_attendances = Attendance.objects.filter(match=match).values_list('player_id', flat=True)

    if request.method == 'POST':
        selected_player_ids = request.POST.getlist('players')

        # Remove all current attendances
        Attendance.objects.filter(match=match).delete()

        # Create new attendances for selected players
        for player_id in selected_player_ids:
            Attendance.objects.create(match=match, player_id=player_id, present=True)

        return redirect('planner:match-detail', slug=match.slug)

    context = {
        'match': match,
        'all_players': all_players,
        'current_attendances': set(current_attendances),  # Convert to set for faster lookup
    }
    return render(request, 'matches/edit-match-team.html', context)

@login_required
def select_players(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    print(match.team1)
    players = match.team1.players.all()
    print(players)
    attendances = Attendance.objects.filter(match=match)

    if request.method == 'POST':
        selected_player_ids = request.POST.getlist('players')
        Attendance.objects.filter(match=match).delete()
        for player_id in selected_player_ids:
            Attendance.objects.create(match=match, player_id=player_id, present=False)
        return redirect('planner:match-detail', slug=match.slug)

    context = {
        'match': match,
        'players': players,
        'attendances': {a.player_id: a.present for a in attendances},
    }
    return render(request, 'matches/select-players.html', context)


@login_required
@require_POST
@csrf_exempt
def delete_match(request, slug):
    match = Match.objects.get(slug=slug)
    match.delete()
    matches = Match.objects.all()
    return render(request, 'matches/partials/matches-table-body.html', {'matches': matches})


### TEAMS
@login_required
def team_index(request):
    teams = Team.objects.all()
    return render(request, 'teams/teams.html', {'teams': teams})

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save()
            selected_player_ids = request.POST.getlist('selected_players')
            selected_players = Player.objects.filter(id__in=selected_player_ids)
            team.players.add(*selected_players)
            request.session['selected_players'] = []
            return redirect('planner:team-index')
    else:
        form = TeamCreateForm()
        selected_player_ids = request.session.get('selected_players', [])
        selected_players = Player.objects.filter(id__in=selected_player_ids)
        all_players = Player.objects.all()

    return render(request, 'teams/create-team.html', {
        'form': form,
        'selected_players': selected_players,
        'players': all_players
    })

@login_required
def search_players(request):
    query = request.GET.get('search', '')
    team_id = request.GET.get('team_id')

    if team_id:
        team = get_object_or_404(Team, id=team_id)
        selected_players = team.players.all()
        if query:
            players = Player.objects.filter(name__icontains=query).exclude(id__in=selected_players)
        else:
            players = Player.objects.exclude(id__in=selected_players)
    else:
        selected_player_ids = request.session.get('selected_players', [])
        if query:
            players = Player.objects.filter(name__icontains=query).exclude(id__in=selected_player_ids)
        else:
            players = Player.objects.exclude(id__in=selected_player_ids)

    context = {
        'players': players,
        'selected_players': selected_player_ids if not team_id else list(selected_players.values_list('id', flat=True)),
    }
    if team_id:
        context['team'] = team

    return render(request, 'teams/partials/players-list.html', context)

@login_required
def add_player(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        action = request.POST.get('action')
        team_id = request.POST.get('team_id')

        if team_id:
            team = get_object_or_404(Team, id=team_id)
            if action == 'add':
                team.players.add(player_id)
            elif action == 'remove':
                team.players.remove(player_id)
                if team.captain_id == int(player_id):
                    team.captain = None
                    team.save()
            selected_players = team.players.all()
        else:
            if 'selected_players' not in request.session:
                request.session['selected_players'] = []

            selected_players = request.session['selected_players']

            if action == 'add' and player_id not in selected_players:
                selected_players.append(player_id)
            elif action == 'remove' and player_id in selected_players:
                selected_players.remove(player_id)

            request.session['selected_players'] = selected_players
            request.session.modified = True
            selected_players = Player.objects.filter(id__in=selected_players)


        all_players = Player.objects.all()

        context = {
            'selected_players': selected_players,
            'players': all_players,
        }
        if team_id:
            context['team'] = team

        return render(request, 'teams/partials/player-lists-container.html', context)

    return HttpResponse(status=400)

@login_required
def nominate_captain(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        team_id = request.POST.get('team_id')
        action = request.POST.get('action')

        player = get_object_or_404(Player, id=player_id)
        team = get_object_or_404(Team, id=team_id)

        toast_message = ''
        toast_type = 'info'

        with transaction.atomic():
            if action == 'nominate':
                if team.captain and team.captain != player:
                    toast_message = 'A captain has already been nominated for this team.'
                    toast_type = 'error'
                else:
                    if team.captain:
                        team.captain.role = 'PL'
                        team.captain.save()

                    team.captain = player
                    player.role = 'CP'
                    player.save()
                    team.save()
                    toast_message = f'{player.name} has been nominated as captain.'
                    toast_type = 'success'
            elif action == 'remove':
                if team.captain == player:
                    team.captain = None
                    player.role = 'PL'
                    player.save()
                    team.save()
                    toast_message = f'{player.name} has been removed as captain.'
                    toast_type = 'success'
                else:
                    toast_message = f'{player.name} is not the current captain.'
                    toast_type = 'error'

        # Re-render the entire player lists container
        context = {
            'selected_players': team.players.all(),
            'players': Player.objects.exclude(id__in=team.players.all()),
            'team': team,
            'toast_message': toast_message,
            'toast_type': toast_type,
        }
        updated_html = render_to_string('teams/partials/player-lists-container.html', context, request=request)

        return HttpResponse(updated_html)

    return HttpResponse('Invalid request method', status=400)

@login_required
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = TeamCreateForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save()
            selected_player_ids = request.POST.getlist('selected_players')
            print(f'selected_players: {selected_player_ids}')
            selected_players = Player.objects.filter(id__in=selected_player_ids)
            team.players.add(*selected_players)
            return redirect('planner:team-index')
    else:
        form = TeamCreateForm(instance=team)
        print(form.fields['subchampionship'].choices)



    selected_players = team.players.all()
    all_players = Player.objects.all()

    context = {
        'form': form,
        'team': team,
        'selected_players': selected_players,
        'players': all_players,
    }
    return render(request, 'teams/edit-team.html', context)


@login_required
def load_subchampionships(request):
    championship_id = request.GET.get('championship')
    subchampionships = SubChampionship.objects.filter(championship_id=championship_id).order_by('name')
    return render(request, 'teams/partials/subchampionship-options.html', {'subchampionships': subchampionships})


@require_POST
@csrf_exempt
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    teams = Team.objects.all()
    return render(request, 'teams/partials/team-table-body.html', {'teams': teams})


### ATTENDANCES
@require_POST
def send_confirmation_email(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)

    if attendance.email_status == 'CONFIRMED':
        return JsonResponse({'status': 'info', 'message': 'Attendance already confirmed'})

    token = generate_token(attendance_id)
    confirmation_url = request.build_absolute_uri(
        reverse('planner:confirm_attendance', args=[token])
    )

    subject = f"Confirmation de présence - Match {attendance.match}"
    message = f"""
    Bonjour {attendance.player.name},

    Veuillez confirmer votre présence pour le match {attendance.match} en cliquant sur le lien suivant:
    {confirmation_url}

    Merci,
    L'équipe de gestion
    """

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [attendance.player.email],
            fail_silently=False,
        )
        attendance.email_status = 'SENT'
        attendance.last_email_sent = timezone.now()
        attendance.save()
        return JsonResponse({'status': 'success', 'message': 'Email sent successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@require_GET
def confirm_attendance(request, token):
    attendance_id = validate_token(token)
    if attendance_id:
        attendance = get_object_or_404(Attendance, id=attendance_id)
        attendance.present = True
        attendance.email_status = 'CONFIRMED'
        attendance.save()
        return render(request, 'utils/attendance-confirmed.html', {'attendance': attendance})
    else:
        return render(request, 'utils/invalid-token.html')


@require_POST
def confirm_attendance_manual(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    attendance.present = True
    attendance.email_status = 'CONFIRMED'
    attendance.save()
    return JsonResponse({'status': 'success', 'message': 'Attendance confirmed successfully'})


@require_POST
def remove_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    attendance.present = False
    attendance.save()
    return JsonResponse({'status': 'success', 'message': 'Attendance removed successfully'})


# Search
@login_required
def search(request):
    query = request.GET.get('q', '')
    teams = Team.objects.filter(name__icontains=query)[:5]
    matches = Match.objects.filter(
        Q(team1__name__icontains=query) |
        Q(team2__icontains=query)
    )[:5]

    team_results = [{'id': team.id, 'name': team.name} for team in teams]
    match_results = [{'slug': match.slug, 'team1': str(match.team1), 'team2': match.team2} for match in matches]

    return JsonResponse({
        'teams': team_results,
        'matches': match_results,
    })
