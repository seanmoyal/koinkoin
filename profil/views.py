from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from profil.models import Team, Team_request

from accounts.models import CUser


def page_profil(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    refresh_rank(request)
    teams = Team.objects.filter(joueurs=user)
    return render(request, 'profil/page-profil.html',{"user" : user,"teams":teams})







def creer_team(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        nom_team = request.POST.get('teamname')
        affiliation = request.POST.get('affiliation')
        if affiliation == user.username:
            return redirect('creer-team')
        elif CUser.objects.filter(username=affiliation).count()==0:
            return redirect('creer-team')
        elif CUser.objects.get(username=affiliation).has_team:
            return redirect('creer-team')
        team = Team_request.objects.create(nom_team=nom_team,demandeur=user.username,demandé=affiliation)
        team.joueurs.add(user)
        team.joueurs.add(CUser.objects.get(username = affiliation))
        refresh_rank(request)
        return redirect('page-profil')
    refresh_rank(request)
    return render(request,'profil/creer-team.html')


def team_request(request):
    user =request.user
    if not user.is_authenticated:
        return redirect('login')
    # suite à changer en mieux
    demandes = Team_request.objects.filter(joueurs=user)
    refresh_rank(request)
    return render(request,'profil/ajout-team.html',context = {'demandes' : demandes})

## RAJOUTER DES LIGNES POUR S ASSURER QUE LA PERSONNE DEMANDEE ET AUSSI LA DEMANDEUSE EST A TOUT MOMENT DANS AUCUNE TEAM

def annule_team_request(request,nom_team):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    team = Team_request.objects.get(nom_team=nom_team)
    team.delete()
    refresh_rank(request)
    return redirect('ajout-team')

def refuse_team_request(request,nom_team):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    team = Team_request.objects.get(nom_team=nom_team)
    team.delete()
    refresh_rank(request)
    return redirect('ajout-team')

def accept_team_request(request,nom_team):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    team_validee = Team_request.objects.get(nom_team=nom_team)
    joueur2 = CUser.objects.get(username=team_validee.demandeur)
    points = 0.5*int(user.points+joueur2.points)
    nouvelle_team = Team.objects.create(nom_team=nom_team, joueur1=user.username, joueur2=joueur2.username, points= points)
    nouvelle_team.joueurs.add(user)
    nouvelle_team.joueurs.add(joueur2)
    teams = Team_request.objects.filter(joueurs=user)

    for team in teams:
        team.delete()
    teams_demandeur = Team_request.objects.filter(joueurs=joueur2)
    for team in teams_demandeur:
        team.delete()

    user.has_team = True
    joueur2.has_team = True
    user.save()
    joueur2.save()
    refresh_rank(request)
    return redirect('page-profil')
'''
def accept_invite(request):# accepter l'invitation en team
    if request.method == "POST":
        pass

def refuse_invite(request): # refuser l'invitation en team
    if request.method == "POST":
        return redirect('page-profil')
    return redirect('page-profil')
'''





def player_detail(request,joueur_recherche):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    refresh_rank(request)
    joueur = CUser.objects.get(username=joueur_recherche)

    return render(request,'profil/player-detail.html',{"joueur":joueur})


def ranking(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    refresh_rank(request)
    if request.method == "POST":
        joueur_recherche = request.POST.get('recherche')
        joueur = CUser.objects.filter(username=joueur_recherche)
        if joueur.count() == 0:
            return redirect('ranking')
        else:
           return redirect('player-detail',joueur_recherche=joueur_recherche)

    # trouver la fonction qui ordonne par le nombre de points
    joueurs = CUser.objects.order_by('-points')

    return render(request,'profil/ranking.html',context={'joueurs' : joueurs} )

def redirect_to_profil(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    return redirect('page-profil')

def quitter_team(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    team = Team.objects.get(joueurs=user)
    us1=CUser.objects.get(username=team.joueur1)
    us2=CUser.objects.get(username=team.joueur2)
    team.delete()
    us1.has_team = False
    us1.save()
    us2.has_team = False
    us2.save()
    refresh_rank(request)
    return redirect('page-profil')

def refresh_rank(request):
    all_players = CUser.objects.order_by('-points')
    for player in all_players:
        index = (*all_players,).index(player)
        player.rank = index + 1
        player.save()