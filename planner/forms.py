from datetime import date

from django import forms
from django.urls import reverse_lazy

from planner.models import Team, Match, SubChampionship, Championship


class ChampionshipForm(forms.ModelForm):
    class Meta:
        model = Championship
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6',
                'placeholder': 'Championship Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6',
                'placeholder': 'Championship Description',
                'rows': 3
            }),
        }

class SubChampionshipForm(forms.ModelForm):
    class Meta:
        model = SubChampionship
        fields = ['name', 'championship', 'required_players']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6',
                'placeholder': 'SubChampionship Name'
            }),
            'championship': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6 [&_*]:text-black'
            }),
            'required_players': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6',
                'placeholder': 'Required Players'
            }),
        }





class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'championship', 'subchampionship']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6'}),
            'championship': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6 [&_*]:text-black',
                'hx-get': reverse_lazy('planner:load-subchampionships'),
                'hx-target': '#id_subchampionship',
                'hx-trigger': 'change'}),
            'subchampionship': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6 [&_*]:text-black'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'championship' in self.data:
            try:
                championship_id = int(self.data.get('championship'))
                self.fields['subchampionship'].queryset = SubChampionship.objects.filter(championship_id=championship_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subchampionship'].queryset = self.instance.championship.subchampionships.all().order_by('name') if self.instance.championship else SubChampionship.objects.none()

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team1', 'team2', 'date', 'championship', 'subchampionship']
        widgets = {
            'team1': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6 [&_*]:text-black'}),
            'team2': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6 [&_*]:text-black'}),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6 [&_*]:text-black'},
                format='%Y-%m-%d'),
            'championship': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6 [&_*]:text-black'}),
            'subchampionship': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-orange-500 sm:text-sm sm:leading-6 [&_*]:text-black'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subchampionship'].queryset = SubChampionship.objects.none()

        if 'championship' in self.data:
            try:
                championship_id = int(self.data.get('championship'))
                self.fields['subchampionship'].queryset = SubChampionship.objects.filter(championship_id=championship_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.championship:
            self.fields['subchampionship'].queryset = self.instance.championship.subchampionships.all()
