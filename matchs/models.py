from django.db import models
from django.shortcuts import get_object_or_404
from datetime import datetime
from profil.models import Team

from accounts.models import CUser


class Match_a_venir(models.Model):
    demandeur = models.CharField(max_length=50)
    demandé = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team)
    def __str__(self):
        return self.demandeur +" vs "+ self.demandé

class Match_passé(models.Model):
    victoire = models.CharField(max_length=50)
    defaite = models.CharField(max_length=50)
    joueurs = models.ManyToManyField(CUser)
    joueur_victorieux1=models.CharField(max_length=50,default="")
    joueur_victorieux2=models.CharField(max_length=50,default="")
    joueur_defait1=models.CharField(max_length=50,default="")
    joueur_defait2=models.CharField(max_length=50,default="")
    date = models.DateTimeField(default=datetime.today().date())
    pts_gagnants=models.IntegerField(default=0)
    pts_defaits = models.IntegerField(default=0)
    def __str__(self):
        return self.victoire +" vs "+ self.defaite

# dans matchs passés rajouter les 4 joueurs leur rang et leurs pts, l'importance n'est pas la team puisque ca casse rapidement


class Match_en_cours(models.Model):
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team)
    date = models.DateTimeField(default=datetime.now())
    victoire = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.team1 +" vs "+ self.team2

