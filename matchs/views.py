from django.shortcuts import render, redirect

from matchs.models import Match_a_venir,Match_passé,Match_en_cours

from profil.models import Team

from profil.views import refresh_rank

from accounts.models import CUser


def go_to_matchs(request): ## A changer pour y accèder sans équipe
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    matchs_passes = Match_passé.objects.filter(joueurs=user).order_by("-date")
    if user.has_team:
        team_user = Team.objects.get(joueurs=user)
        match_en_cours = Match_en_cours.objects.filter(teams=team_user)
        return render(request,'matchs/matchs.html',{"match_en_cours":match_en_cours,"matchs_passes" : matchs_passes,"team_user":team_user,"user":user})
    return render(request,'matchs/matchs.html',{"matchs_passes" : matchs_passes})

def proposer_match(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.has_team:
        return redirect('page-profil')
    if request.method == 'POST':
        nom_team = request.POST.get('teamname')
        team_user = Team.objects.get(joueurs=user)
        if nom_team == team_user.nom_team:
            return redirect('proposer-match')
        elif Team.objects.filter(nom_team=nom_team).count() == 0:
            return redirect('proposer-match')
        if Match_a_venir.objects.filter(demandeur=team_user.nom_team).count() == 0:
            match = Match_a_venir.objects.create(demandeur=team_user.nom_team,demandé=nom_team)
            match.teams.add(team_user)
            match.teams.add(Team.objects.get(nom_team=nom_team))
            return redirect('matchs')
        else :
            return redirect('matchs')
    return render(request,'matchs/proposermatch.html')

def demandes_match(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.has_team:
        return redirect('page-profil')
    team_user = Team.objects.get(joueurs=user)
    demandes = Match_a_venir.objects.filter(teams=team_user)
    return render(request,'matchs/demandesmatch.html',context = {'demandes' : demandes,'team':team_user})

def accepter_demande_match(request,demandeur):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.has_team:
        return redirect('page-profil')
    match_validé = Match_a_venir.objects.get(demandeur=demandeur)
    team1 = Team.objects.get(nom_team=demandeur)
    team2=Team.objects.get(joueurs=user)
    match_en_cours = Match_en_cours.objects.create(team1=team1.nom_team, team2=team2.nom_team)
    match_en_cours.teams.add(team1)
    match_en_cours.teams.add(team2)
    demandes = Match_a_venir.objects.filter(teams=team1)
    for demande in demandes:
        demande.delete()
    demandes2 = Match_a_venir.objects.filter(teams=team2)
    for demande in demandes2:
        demande.delete()

    refresh_rank(request)
    return redirect('matchs')


def refuser_demande_match(request,demandeur):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.has_team:
        return redirect('page-profil')
    demande_match = Match_a_venir.objects.get(demandeur=demandeur)
    demande_match.delete()
    return redirect('matchs')


def annuler_demande_match(request,demandeur):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.has_team:
        return redirect('page-profil')
    demande_match = Match_a_venir.objects.get(demandeur=demandeur)
    demande_match.delete()
    return redirect('matchs')


def victoire_team1(request,team1):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.has_team:
        return redirect('page-profil')
    team_user=Team.objects.get(joueurs=user)
    match = Match_en_cours.objects.get(teams=team_user)
    match.victoire=team1
    match.save()
    return redirect('matchs')

def victoire_team2(request,team2):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.has_team:
        return redirect('page-profil')
    team_user=Team.objects.get(joueurs=user)
    match = Match_en_cours.objects.get(teams=team_user)
    match.victoire=team2
    match.save()
    return redirect('matchs')

def confirmer_victoire(request,victoire):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.has_team:
        return redirect('page-profil')
    team_victorieuse = Team.objects.get(nom_team=victoire)
    joueur_victorieux1 = CUser.objects.get(username=team_victorieuse.joueur1)
    joueur_victorieux2 = CUser.objects.get(username=team_victorieuse.joueur2)

    match = Match_en_cours.objects.get(teams=team_victorieuse)
    team1 = match.team1
    team2 = match.team2
    team_defaite=""
    if team1 == victoire:
        team_defaite = team2
    else:
        team_defaite = team1
    defaite=Team.objects.get(nom_team=team_defaite)
    joueur_defait1= CUser.objects.get(username=defaite.joueur1)
    joueur_defait2 = CUser.objects.get(username=defaite.joueur2)

    match_fini = Match_passé.objects.create(date=match.date, victoire=victoire, defaite=team_defaite,joueur_defait1=joueur_defait1.username,joueur_defait2=joueur_defait2.username,joueur_victorieux1=joueur_victorieux1.username,joueur_victorieux2=joueur_victorieux2.username)
    match_fini.joueurs.add(joueur_victorieux1)
    match_fini.joueurs.add(joueur_victorieux2)
    match_fini.joueurs.add(joueur_defait1)
    match_fini.joueurs.add(joueur_defait2)
    match_fini.save()
    match.delete()
    pts_defaite=defaite.points
    pts_gagnant=team_victorieuse.points
    pts_additionnés,pts_soustraits = calcul_gain_perte(pts_gagnant,pts_defaite)
    team_victorieuse.points+=pts_additionnés
    defaite.points+=pts_soustraits
    team_victorieuse.save()
    defaite.save()
    match_fini.pts_gagnants=pts_additionnés
    match_fini.pts_defaits=pts_soustraits
    match_fini.save()
    joueur_defait1.points+=pts_soustraits
    joueur_defait2.points += pts_soustraits
    joueur_victorieux1.points+=pts_additionnés
    joueur_victorieux2.points+=pts_additionnés
    joueur_defait1.save()
    joueur_defait2.save()
    joueur_victorieux1.save()
    joueur_victorieux2.save()
    return redirect('matchs')

def contester_victoire(request,victoire):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.has_team:
        return redirect('page-profil')
    match = Match_en_cours.objects.get(victoire=victoire)
    match.victoire=""
    match.save()
    return redirect('matchs')


def calcul_gain_perte(pts_gagnants,pts_perdants):
    ecart = pts_gagnants - pts_perdants
    if ecart>=-20:
        return (10,-5)
    elif -20 > ecart >= -100:
        return(+int(ecart/3),-int(ecart/4))
    else:
        return (+33,-25)
