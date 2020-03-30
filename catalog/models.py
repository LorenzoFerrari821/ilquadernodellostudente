from django.db import models
from django.core.validators import FileExtensionValidator,MinValueValidator,MaxValueValidator
from users.models import Profile



# Create your models here.




class Item(models.Model):               #Modello dell'oggetto
    SCHOOL_LEVEL = (
        ('M', 'Medie'),
        ('S', 'Superiori'),
        ('U', 'Università'),
    )
    vendor=models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,verbose_name="Venditore")               #Colui che vende l'oggetto
    name = models.CharField(max_length=50,verbose_name="Nome")
    description=models.TextField(max_length=1000,verbose_name="Descrizione dell'oggetto")
    subject=models.CharField(max_length=30,verbose_name="Materia/disciplina")                                #materia
    school_level=models.CharField(max_length=1,choices=SCHOOL_LEVEL,verbose_name="Livello scolastico")                  #media, superiore, università
    is_visible=models.BooleanField(default=True)                                                          #Se l'utente ha cancellato l'oggetto dalla vendita, non è più visibile nel catalogo e quindi non più acquistabile
    vote=models.DecimalField(max_digits=2,decimal_places=1,default=0,validators=[MinValueValidator(0,'Il voto minimo non può essere minore di 0'),MaxValueValidator(5,"Il voto massimo non può essere più di 5")],verbose_name="Voto")
    price= models.DecimalField(max_digits=6, decimal_places=2,validators=[MinValueValidator(2,'Il prezzo minimo non può essere minore di 2€')],verbose_name="Prezzo di vendita")    #Validator per prezzo minimo >= 2
    image=models.FileField(verbose_name="Immagine di anteprima",help_text='Si consiglia fortemente l\'uso di immagini di dimensioni 400x400 px',upload_to='item/preview',validators=[FileExtensionValidator(['png','jpg','jpeg'],'Formato non valido. Inserisci una immagine con uno dei seguenti formati: jpg,jpeg,png')])       #Validator per estensione
    file=models.FileField(help_text="E' obbligatorio l'uso del formato pdf.",upload_to='item/files',validators=[FileExtensionValidator(['pdf'],'Formato non valido. Inserisci un file in formato pdf')])            #Validator per estensione

    def __str__(self):
        return self.name

class HaveItem(models.Model):                   #Associa ogni utente alla lista di oggetti che ha comprato, in modo da permettergli di scaricarli in futuro
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    itemspurchased = models.ManyToManyField(Item, blank=True)               #Lista oggetti comprati

    def __str__(self):
        return "Lista oggetti comprati da:" + self.profile.user.username

class ReviewsObject(models.Model):              #Associa ogni utente alla lista degli oggetti che ha recensito, per controlare che ogni oggetto venga recensito solo una volta per utente
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    reviewed_object = models.ManyToManyField(Item, blank=True)  # Lista oggetti recensiti

    def __str__(self):
        return "Lista oggetti recensiti da:" + self.profile.user.username
