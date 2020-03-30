from django.conf.urls import url
from . import views

app_name='checkout'

urlpatterns = [
    url(r'^$', views.cart, name='Cart'),                                                                                #Mostra carrello
    url(r'^additem/(?P<item_id>[0-9]+)/$',views.additem,name='Additem'),                                                #Mostra la pagina per aggiungere un oggetto al carrello
    url(r'^deleteitem/(?P<item_id>[0-9]+)/$',views.deleteitem,name='Deleteitem'),                    #Elimina un oggetto dal carrello
    url(r'^payment/(?P<cart_id>[0-9]+)$',views.payment,name="Payment"),                                                 #Gestione pagamenti
    url(r'^retrieve/(?P<item_id>[0-9]+)$',views.retrieve,name="Retrieve"),                                              #View per download oggetti
    url(r'^placeorder/(?P<cart_id>[0-9]+)$',views.placeorder,name="Placeorder")                                         #Conferma l'acquisto
]
