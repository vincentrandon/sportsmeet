import datetime
import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


class PlayerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email doit être renseigné")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Player(AbstractBaseUser, PermissionsMixin):

    ROLE = (
        ('CP', 'Captain'),
        ('PL', 'Player'),
    )

    name = models.CharField(max_length=100)
    licence_number = models.CharField(max_length=100)
    role = models.CharField(max_length=2, choices=ROLE, default='PL')
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = PlayerManager()


    def __str__(self):
        return self.name

    def get_full_name(self):
        return f"{self.name}"

    def get_initals(self):
        return "".join([name[0] for name in self.name.split()])

    def get_role_display(self):
        return dict(self.ROLE)[self.role]



class Championship(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class SubChampionship(models.Model):
    name = models.CharField(max_length=100)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name='subchampionships')
    required_players = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.championship.name})"


class Team(models.Model):
    name = models.CharField(max_length=100)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    subchampionship = models.ForeignKey(SubChampionship, on_delete=models.CASCADE, null=True, blank=True)
    players = models.ManyToManyField(Player, related_name='teams')
    captain = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='captain_of')

    def __str__(self):
        return f'{self.name} - {self.championship}'









class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.CharField(max_length=100)
    occurrence = models.CharField(max_length=100, blank=True)
    date = models.DateField(default=datetime.date.today)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, blank=True, null=True)
    subchampionship = models.ForeignKey(SubChampionship, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.team2:
            return f"{self.team1} vs {self.team2}"
        else:
            return f"{self.team1} vs TBA"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.team1} vs {self.team2} {self.date}')
        if not self.championship and self.team1.championship:
            self.championship = self.team1.championship
        if not self.subchampionship and self.team1.subchampionship:
            self.subchampionship = self.team1.subchampionship
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return f'/matches/{self.slug}'


class Attendance(models.Model):
    EMAIL_STATUS_CHOICES = [
        ('NOT_SENT', 'Not Sent'),
        ('SENT', 'Sent'),
        ('CONFIRMED', 'Confirmed'),
    ]

    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    email_status = models.CharField(max_length=10, choices=EMAIL_STATUS_CHOICES, default='NOT_SENT')
    last_email_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.player} - {self.match}"