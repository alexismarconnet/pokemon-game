from django import forms
 
from .models import Character
from .models import Dresseur

POKEMON_CHOICES = [
    ("Salamèche", "Salamèche"),
    ("Bulbizarre", "Bulbizarre"),
    ("Carapuce", "Carapuce"),
]

class CreateDresseurForm(forms.ModelForm):
    pokemon_initial = forms.ChoiceField(choices=POKEMON_CHOICES,
        label="Choisissez votre Pokémon initial",
        widget=forms.RadioSelect
    )

    class Meta:
        model = Dresseur
        fields = ['nom', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du dresseur'}),
            'photo': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de la photo'}),
        }
        labels = {
            'nom': 'Nom',
            'photo': 'Photo (URL)',
        }


class MoveForm(forms.ModelForm):
 
    class Meta:
        model = Character
        fields = ('lieu',)