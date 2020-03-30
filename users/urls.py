from django.conf.urls import url
from . import views

app_name='users'


urlpatterns = [
    url(r'^$', views.login_view, name='Login'),                                                                         #Pagina di login
    url(r'^(?P<user_id>[0-9]+|None|)/$',views.profile,name='Profile'),                                                  #Mostra il profilo utente
    url(r'^editdata/$',views.editdata,name="Editdata"),                                                                 #Pagina di modifica dati profilo
    url(r'^editimage/$',views.editimage,name="Editimage"),                                                              #Pagina di modifica immagine
    url(r'^editpassword/$',views.editpassword,name="Editpassword"),                                                     #Pagina di cambio password
    url(r'^purchaselist/$',views.purchaselist,name="Purchaselist"),                                                     #Lista degli oggetti acquistati dall'utente
    url(r'^logout/$',views.logout_view,name='Logout'),                                                                  #Pagina di logout
    url(r'^signup/$',views.signup,name='Signup'),                                                                       #Pagina di registrazione
    url(r'^create/$',views.create,name="Create"),                                                                       #Pagina per creazione di nuove inserzioni
    url(r'^selectitem/$',views.selectitem,name="Selectitem"),                                                           #Pagina che mostra gli oggetti su cui è possibile apportare modifiche/eliminare/recensire
    url(r'^deleteitem/(?P<item_id>[0-9]+)/$', views.deleteitem, name="Deleteitem"),                                     #Pagina per eliminazione oggetto
    url(r'^edititem/(?P<item_id>[0-9]+)/$', views.edititem, name="Edititem"),                                           #Pagina per modifica dati oggetto
    url(r'^review/(?P<item_id>[0-9]+)/$', views.review, name="Review"),                                                 #Pagina che permette di lasciare un voto agli oggetti


]
