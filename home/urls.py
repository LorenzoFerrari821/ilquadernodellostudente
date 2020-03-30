from django.conf.urls import url
from . import views

app_name='home'                              #per distinguere questi url/views da altre app (video 21 )


urlpatterns = [
    url(r'^$', views.home, name='Home'),

]
