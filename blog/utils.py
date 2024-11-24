from django.db.models import Count
import random
from .models import Lieu,Character,Badge
from django.contrib import messages
import json
import random
from .models import Character, Lieu
def choisir_pokemon_aleatoire(pokemon_data):
    """
    Choisit un Pokémon au hasard dans un dictionnaire de Pokémon.

    :param pokemon_data: dict - Dictionnaire contenant les données des Pokémon.
    :return: dict - Les informations d'un Pokémon choisi au hasard.
    """
    if not pokemon_data:
        raise ValueError("Le dictionnaire des Pokémon est vide.")
    
    pokemon_aleatoire = random.choice(list(pokemon_data.values()))
    
    if not isinstance(pokemon_aleatoire, dict):
        raise ValueError("Les données des Pokémon ne sont pas au format attendu.")
    
    return pokemon_aleatoire
def rencontrer_pokemon_sauvage(dresseur):
    # Chemin vers le fichier JSON contenant les Pokémon
    fichier_pokemon = 'blog/pokemon_1g_with_types.json'

    # Charger les données JSON
    with open(fichier_pokemon, 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)

    pokemon_aleatoire = random.choice(list(pokemon_data.values()))

    # Créer un lieu "Dans sa pokeball" s'il n'existe pas encore
    lieu, created = Lieu.objects.get_or_create(
        id_lieu="Dans sa pokeball",
        defaults={"disponibilite": "libre", "photo": ""}
    )

    # Créer le Pokémon sauvage dans la base de données
    pokemon_sauvage = Character.objects.create(
        id_character=pokemon_aleatoire['id_character'],
        etat="En pleine santé",
        type=pokemon_aleatoire['type'],
        team="Sauvage",
        photo=pokemon_aleatoire['photo'],
        lieu=lieu,
        dresseur=None  # Pas encore capturé
    )

    # Retourner un dictionnaire avec les détails du Pokémon sauvage
    return {
        "id_character": pokemon_sauvage.id_character,
        "type": pokemon_sauvage.type,
        "etat": pokemon_sauvage.etat,
        "photo": pokemon_sauvage.photo,
        "team": pokemon_sauvage.team,
        "lieu": pokemon_sauvage.lieu.id_lieu,
    }

def mettre_a_jour_disponibilite_lieux(): 
    from .models import Lieu, Character  # Importez vos modèles ici

    # Rendre le Centre toujours libre
    centre = Lieu.objects.filter(id_lieu="Centre").first()
    if centre:
        centre.disponibilite = "libre"
        centre.save()

    # Vérifier tous les autres lieux
    for lieu in Lieu.objects.exclude(id_lieu="Centre"):
        # Compter les Pokémon dans ce lieu
        nb_pokemon = Character.objects.filter(lieu=lieu).count()

        if lieu.id_lieu == "Playground" and nb_pokemon < 3:
            lieu.disponibilite = "libre"
        elif lieu.id_lieu == "Playground" and nb_pokemon >= 3:
            lieu.disponibilite = "occupé"
        elif nb_pokemon < 1:
            lieu.disponibilite = "libre"
        else:
            lieu.disponibilite = "occupé"

        lieu.save()

def mettre_a_jour_etat_pokemon(character):
    if character.lieu.id_lieu == "Centre":
        character.etat = "En pleine santé"

    elif character.lieu.id_lieu == "Arène 1":
        # 1 chance sur 3 d'être "K.O."
        if random.randint(1, 3) == 1:
            character.etat = "K.O."

    elif character.lieu.id_lieu == "Arène 2":
        # 1 chance sur 2 d'être "Empoisonné"
        if random.randint(1, 2) == 1:
            character.etat = "Empoisonné"

    elif character.lieu.id_lieu == "Playground":
        # 1 chance sur 2 de devenir "Heureux" si "En pleine santé"
        if character.etat == "En pleine santé" and random.randint(1, 2) == 1:
            character.etat = "Heureux"

    character.save()

def gain_badge(character, request):
    import random

    dresseur = character.dresseur  # Récupère le dresseur du Pokémon
    if not dresseur:
        return  # Si le Pokémon n'a pas de dresseur, rien ne se passe

    # Arène 1 : Badge d'Albert
    if character.lieu.id_lieu == "Arène 1" and random.randint(1, 10) == 10:  # 10% de chances
        if not dresseur.badges.filter(nom="Badge d'Albert").exists():
            badge = Badge.objects.create(nom="Badge d'Albert", photo="url_de_l_image_du_badge")
            dresseur.badges.add(badge)
            dresseur.save()
            messages.success(request, f"{dresseur.nom} a gagné le Badge d'Albert grâce à {character.id_character} !")

    # Arène 2 : Badge de Hector
    elif character.lieu.id_lieu == "Arène 2" and random.randint(1, 4) == 1:  # 25% de chances
        if not dresseur.badges.filter(nom="Badge de Hector").exists():
            badge = Badge.objects.create(nom="Badge de Hector", photo="url_de_l_image_du_badge")
            dresseur.badges.add(badge)
            dresseur.save()
            messages.success(request, f"{dresseur.nom} a gagné le Badge de Hector grâce à {character.id_character} !")

    # Arène 3 : Badge de Blanche
    elif character.lieu.id_lieu == "Arène 3" and random.randint(1, 5) == 1:  # 20% de chances
        if not dresseur.badges.filter(nom="Badge de Blanche").exists():
            badge = Badge.objects.create(nom="Badge de Blanche", photo="url_de_l_image_du_badge")
            dresseur.badges.add(badge)
            dresseur.save()
            messages.success(request, f"{dresseur.nom} a gagné le Badge de Blanche grâce à {character.id_character} !")