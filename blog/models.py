from django.db import models

class Dresseur(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    photo = models.URLField(blank=True, null=True)  
    badges = models.ManyToManyField('Badge', blank=True, related_name='dresseurs') 

    def __str__(self):
        return self.nom

class Lieu(models.Model):
    id_lieu = models.CharField(max_length=100, primary_key=True)
    disponibilite = models.CharField(max_length=20)
    photo = models.CharField(max_length=200)
    def __str__(self):
        return self.id_lieu
    
 
 
class Character(models.Model):
    id_character = models.CharField(max_length=100, primary_key=True)
    etat = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    team = models.CharField(max_length=20)
    photo = models.CharField(max_length=200)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
    dresseur = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name="pokemons", null=True, blank=True)
    def __str__(self):
        return self.id_character
    def change_etat(self, nv_etat):
        self.etat=nv_etat
        return "L'état de {self} est désormais {self.etat}"
    
class Badge(models.Model):
    id_badge = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    possede = models.BooleanField(default=False)
    photo = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nom
