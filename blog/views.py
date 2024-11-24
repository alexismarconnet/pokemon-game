from django.shortcuts import render
from .models import Character,Dresseur,Badge
from .models import Lieu  # Exemple : importez vos modèles
from django.utils import timezone
from .forms import MoveForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .utils import mettre_a_jour_disponibilite_lieux
from .utils import mettre_a_jour_etat_pokemon
from django.contrib import messages
from .utils import gain_badge
import random
from .forms import CreateDresseurForm
from .utils import rencontrer_pokemon_sauvage
import json,string
# Vue pour afficher une liste de lieux
def pokemon_list(request):
    character = Character.objects.all()  # Récupère tous les objets de la table Lieu
    return render(request, 'blog/pokemon_list.txt', {'Character': character})
def pokemon_detail(request,pk):
    character=get_object_or_404(Character,pk=pk)
    return render (request,'blog/pokemon_detail.txt',{'character':character})
def Centre(character):
    if character.lieu== "Centre":
        character.etat="En pleine santé"
def dresseur_list(request):
    dresseurs = Dresseur.objects.all()  # Récupère tous les dresseurs
    return render(request, 'blog/dresseur_list.txt', {'dresseurs': dresseurs})

def dresseur_pokemons(request, dresseur_id):
    dresseur = get_object_or_404(Dresseur, id=dresseur_id)
    pokemons = dresseur.pokemons.all()  # Utilisez related_name de la relation ForeignKey
    badges_possedes = dresseur.badges.all()  # Assurez-vous que ceci est correct aussi
    return render(request, "blog/dresseur_pokemons.txt", {
        "dresseur": dresseur,
        "pokemons": pokemons,
        "badges_possedes": badges_possedes,
    })
def relacher_pokemon(request, id_character):
    pokemon = get_object_or_404(Character, id_character=id_character)

    if pokemon.dresseur.pokemons.count() > 1:
        pokemon.delete()  # Supprimer le Pokémon
        messages.success(request, f"{pokemon.id_character} a été relâché avec succès.")
    else:
        messages.error(request, "Vous ne pouvez pas relâcher le dernier Pokémon d'un dresseur.")

    return redirect('dresseur_pokemons', dresseur_id=pokemon.dresseur.id)

from django.db import transaction

def character_detail(request, id_character):
    # Récupérer le personnage
    character = get_object_or_404(Character, id_character=id_character)
    form = MoveForm(instance=character)
    ancien_lieu = character.lieu

    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)
        if form.is_valid():
            # Mise à jour des lieux
            nouveau_lieu = form.cleaned_data['lieu']
            if ancien_lieu:
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()

            character.lieu = nouveau_lieu
            character.save()

            nouveau_lieu.disponibilite = "occupé"
            nouveau_lieu.save()

            messages.success(
                request,
                f"Le lieu de {character.id_character} a été changé avec succès. "
                f"Le Pokémon est maintenant à {nouveau_lieu.id_lieu}."
            )
            return redirect("character_detail", id_character=character.id_character)
        else:
            messages.error(request, "Une erreur est survenue lors du changement de lieu.")

    return render(request, "blog/character_detail.txt", {
        "character": character,
        "form": form,
    })
def creer_dresseur(request):
    if request.method == "POST":
        form = CreateDresseurForm(request.POST)
        if form.is_valid():
            # Créer le dresseur
            dresseur_nom = form.cleaned_data['nom']
            dresseur_photo = form.cleaned_data['photo']
            dresseur = Dresseur.objects.create(
                nom=dresseur_nom,
                photo=dresseur_photo,
            )

            pokemon_nom = form.cleaned_data['pokemon_initial']

            # Caractéristiques des Pokémon
            pokemon_data = {
                "Salamèche": {"type": "Feu", "photo": "https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/004.png"},
                "Bulbizarre": {"type": "Plante", "photo": "https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/001.png"},
                "Carapuce": {"type": "Eau", "photo": "https://www.pokepedia.fr/images/thumb/c/cc/Carapuce-RFVF.png/800px-Carapuce-RFVF.png"},
            }

            data = pokemon_data[pokemon_nom]
            default_lieu = Lieu.objects.get(id_lieu="Maison") 

            # Créer le Pokémon pour le dresseur
            Character.objects.create(
                id_character=pokemon_nom,  # Identifiant du Pokémon
                type=data["type"],        # Type (Feu, Plante, Eau)
                photo=data["photo"],      # URL de l'image
                etat="En pleine santé",   # État initial
                lieu=default_lieu,        # Lieu par défaut
                team="Génération 1",      # Attribut équipe
                dresseur=dresseur,        # Assigner au dresseur nouvellement créé
            )

            messages.success(request, f"Le dresseur {dresseur.nom} a été créé avec son Pokémon {pokemon_nom} !")
            return redirect('dresseur_list')  # Redirection vers la liste des dresseurs
    else:
        form = CreateDresseurForm()

    return render(request, 'blog/creer_dresseur.txt', {'form': form})
def pokemon_sauvage_view(request, id_character):
    # Récupérer le dresseur associé au Pokémon actuellement modifié
    character = get_object_or_404(Character, id_character=id_character)
    dresseur = character.dresseur

    # Générer un Pokémon sauvage aléatoire ou récupérer un Pokémon déjà généré
    if "pokemon_sauvage" not in request.session:
        try:
            with open("blog/pokemon_1g_with_single_type.json", "r", encoding="utf-8") as f:
                pokemon_data = json.load(f)

            # Choisir un Pokémon au hasard
            random_pokemon = random.choice(list(pokemon_data.values()))
            unique_code = ''.join(random.choices(string.digits, k=4))
            unique_id = f"{random_pokemon['id_character']}-{unique_code}"

            # Construire les données du Pokémon sauvage
            pokemon_sauvage = {
                "id_character": unique_id,
                "type": random_pokemon.get("type"),
                "etat": random_pokemon.get("etat", "En pleine santé"),  # Valeur par défaut
                "team": "Sauvage",
                "lieu": "Centre",
                "photo": random_pokemon.get("photo"),
            }

            # Sauvegarder dans la session
            request.session["pokemon_sauvage"] = pokemon_sauvage

        except (FileNotFoundError, json.JSONDecodeError):
            messages.error(request, "Erreur lors du chargement des données des Pokémon sauvages.")
            return redirect("character_detail", id_character=character.id_character)
    else:
        # Charger le Pokémon sauvage depuis la session
        pokemon_sauvage = request.session["pokemon_sauvage"]

    # Si l'utilisateur choisit de capturer
    if request.method == "POST" and "capture" in request.POST:
        with transaction.atomic():
            # Créer le Pokémon capturé
            new_pokemon = Character.objects.create(
                id_character=pokemon_sauvage["id_character"],
                type=pokemon_sauvage["type"],
                etat=pokemon_sauvage["etat"],  # Utilise la clé 'etat'
                team="Capturé",
                lieu=character.lieu,
                photo=pokemon_sauvage["photo"],
                dresseur=dresseur,  # Lien au dresseur actuel
            )
            # Supprimer le Pokémon sauvage de la session après capture
            del request.session["pokemon_sauvage"]

            messages.success(
                request,
                f"Félicitations ! Vous avez capturé {pokemon_sauvage['id_character']} ! "
                f"Il appartient maintenant à {dresseur.nom}."
            )
        return redirect("dresseur_pokemons", dresseur.id)

    # Si l'utilisateur choisit de fuir
    elif request.method == "POST" and "fuite" in request.POST:
        # Supprimer le Pokémon sauvage de la session après fuite
        del request.session["pokemon_sauvage"]
        messages.info(
            request,
            f"Vous avez fui et ignoré {pokemon_sauvage['id_character']}."
        )
        return redirect("character_detail", id_character=character.id_character)

    return render(request, "blog/pokemon_sauvage.txt", {
        "pokemon_sauvage": pokemon_sauvage,
        "character": character,
    })