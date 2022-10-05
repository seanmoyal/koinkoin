from django.contrib import admin

from matchs.models import Match_a_venir, Match_passé, Match_en_cours

admin.site.register(Match_a_venir)
admin.site.register(Match_passé)
admin.site.register(Match_en_cours)