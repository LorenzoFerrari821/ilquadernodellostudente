from django.conf.urls import url
from . import views

app_name='catalog'                              #per distinguere questi url/views da altre app (video 21 )


urlpatterns = [
    url(r'^catalog/$', views.itemlist, name='Itemlist'),                                  #Mostra la lista degli item, tutti oppure solo quelli filtrati
    url(r'^details/(?P<item_id>[0-9]+)/$', views.itemdetail, name="Itemdetail"),          #Porta alla pagina del dettaglio di un preciso item
    url(r'^search/$',views.search,name="Search")                                           #Pagina di ricerca avanzata
]
