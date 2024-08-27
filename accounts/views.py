from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from planner.models import Player


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('planner:index')
        else:
            for error in form.non_field_errors():
                messages.error(request, f"Erreur: {error}")

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Player
    fields = ['name', 'email', 'licence_number']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = "Votre profil a été mis à jour avec succès."

    def get_object(self, queryset=None):
        return self.request.user