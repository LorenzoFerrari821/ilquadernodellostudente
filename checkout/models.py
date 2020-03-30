from django.db import models
from users.models import Profile
from catalog.models import Item



class Cart(models.Model) :                                                                                              #Carrello
    owner=models.OneToOneField(Profile,on_delete=models.CASCADE,verbose_name='Proprietario')
    items=models.ManyToManyField(Item,blank=True)

    def get_cart_items(self):
        return self.items.all()

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.price
        return total

    def __str__(self):
        return "Carrello di: "+self.owner.user.username
