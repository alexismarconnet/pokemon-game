from django.urls import path
from . import views

urlpatterns = [
    path('', views.dresseur_list, name='dresseur_list'),  # Liste des dresseurs
    path('character/<str:id_character>/', views.character_detail, name='character_detail'),  # Détails d'un Pokémon
    path('dresseur/<int:dresseur_id>/', views.dresseur_pokemons, name='dresseur_pokemons'),  # Pokémon d'un dresseur
    path('pokemon_list/', views.pokemon_list, name='pokemon_list'),  # Liste de tous les Pokémon
    path('character/<str:id_character>/relacher/', views.relacher_pokemon, name='relacher_pokemon'),  # Relâcher un Pokémon
    path('creer_dresseur/', views.creer_dresseur, name='creer_dresseur'),  # Création de dresseur
    path('pokemon_sauvage/<str:id_character>/', views.pokemon_sauvage_view, name='pokemon_sauvage_view'),
     ]