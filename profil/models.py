from django.db import models

from accounts.models import CUser


class Team(models.Model):
    nom_team = models.CharField(max_length=50)
    joueurs = models.ManyToManyField(CUser)
    points = models.IntegerField(default=500)
    joueur1 = models.CharField(max_length=50,default="")
    joueur2 = models.CharField(max_length=50,default="")
    rank = models.IntegerField(default=-1)
    # trouver comment affilier deux individus à une même team ( sans doute one_to_many )

    def __str__(self):
        return self.nom_team

class Team_request(models.Model):
    nom_team = models.CharField(max_length=50)
    joueurs = models.ManyToManyField(CUser)
    demandeur = models.CharField(max_length=50,default="")
    demandé = models.CharField(max_length=50,default="")

    def __str__(self):
        return self.nom_team

