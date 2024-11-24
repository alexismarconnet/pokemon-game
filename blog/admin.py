from django.contrib import admin

from .models import Character,Lieu,Badge, Dresseur

admin.site.register(Character)
admin.site.register(Lieu)
admin.site.register(Badge)
admin.site.register(Dresseur)