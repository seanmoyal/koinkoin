from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from accounts.views import signup, logout_user, login_user
from profil.views import page_profil,creer_team,ranking,redirect_to_profil,team_request,accept_team_request,annule_team_request,refuse_team_request,quitter_team,player_detail
from matchs.views import go_to_matchs,proposer_match,demandes_match,accepter_demande_match,refuser_demande_match,annuler_demande_match,victoire_team1,victoire_team2,confirmer_victoire,contester_victoire
from reglementation.views import reglementation
urlpatterns = [
    path('', redirect_to_profil, name='index'),
    path('reglementation', reglementation, name='reglementation'),
    path('profil/', page_profil, name='page-profil'),
    path('matchs/', go_to_matchs, name='matchs'),
    path('ranking/', ranking, name='ranking'),
    path('creation-team/', creer_team, name='creer-team'),
    path('ajout-team/', team_request, name='ajout-team'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('admin/', admin.site.urls),
    path('ajout-team/refuser/<str:nom_team>/', accept_team_request,name='accept-team-request'),
    path('ajout-team/accepter/<str:nom_team>/', refuse_team_request,name='refuse-team-request'),
    path('ajout-team/annuler/<str:nom_team>/', annule_team_request,name='annule-team-request'),
    path('ranking/<str:joueur_recherche>/', player_detail,name='player-detail'),
    path('ajout-team/quitter-team/', quitter_team,name='quitter-team'),
    path('matchs/proposer-match/', proposer_match, name='proposer-match'),
    path('matchs/demandes-match/', demandes_match, name='demandes-match'),
    path('matchs/demandes-match/accepter/<str:demandeur>', accepter_demande_match, name='accepter-demande-match'),
    path('matchs/demandes-match/refuser/<str:demandeur>', refuser_demande_match, name='refuser-demande-match'),
    path('matchs/demandes-match/annuler/<str:demandeur>', annuler_demande_match, name='annuler-demande-match'),
    path('matchs/victoire-team1/<str:team1>/', victoire_team1, name='victoire-team1'),
    path('matchs/victoire-team2/<str:team2>', victoire_team2, name='victoire-team2'),
    path('matchs/confirmer-victoire/<str:victoire>/', confirmer_victoire, name='confirmer-victoire'),
    path('matchs/contester-victorie/<str:victoire>', contester_victoire, name='contester-victoire'),


]
