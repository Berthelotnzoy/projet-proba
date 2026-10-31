from django.db import models

# Create your models here.
class Photo(models.Model):
    titre = models.CharField(max_length=100, blank=True, null=True, verbose_name="Titre de la photo")
    image = models.ImageField(upload_to='photos/', verbose_name="Fichier image")
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    def __str__(self):
        return self.titre if self.titre else f"Photo {self.id}"