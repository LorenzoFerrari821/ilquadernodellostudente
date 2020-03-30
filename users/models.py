from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class Profile(models.Model):                                                                                            #Estende il modello user
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    qualification=models.CharField(max_length=30,verbose_name="Titolo di studio",blank=True,help_text='Inserisci il più alto titolo di studio ottenuto')
    image = models.FileField(verbose_name="Immagine di profilo",upload_to='profile',blank=True,help_text='Si consiglia fortemente l\'uso di immagini di dimensioni 400x400 px', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'],'Formato non valido. Inserisci una immagine con uno dei seguenti formati: jpg,jpeg,png')])

    def __str__(self):
        return self.user.username




