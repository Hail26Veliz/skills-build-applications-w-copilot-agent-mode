from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection

from djongo import models

# MODELOS SIMPLES PARA POBLAR
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    user = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    score = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Eliminar datos existentes
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()

        # Equipos
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Usuarios
        users = [
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': 'DC'},
        ]
        for u in users:
            User.objects.create_user(username=u['username'], email=u['email'], password='password')

        # Actividades
        Activity.objects.create(name='Correr', user='spiderman', team='Marvel')
        Activity.objects.create(name='Nadar', user='ironman', team='Marvel')
        Activity.objects.create(name='Volar', user='superman', team='DC')
        Activity.objects.create(name='Entrenar', user='batman', team='DC')

        # Leaderboard
        Leaderboard.objects.create(user='spiderman', team='Marvel', score=100)
        Leaderboard.objects.create(user='ironman', team='Marvel', score=90)
        Leaderboard.objects.create(user='batman', team='DC', score=95)
        Leaderboard.objects.create(user='superman', team='DC', score=110)

        # Workouts
        Workout.objects.create(name='Pushups', description='20 pushups', user='spiderman')
        Workout.objects.create(name='Flight', description='Fly for 10 minutes', user='superman')
        Workout.objects.create(name='Gadgets', description='Train with gadgets', user='batman')
        Workout.objects.create(name='Armor', description='Test new armor', user='ironman')

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))
