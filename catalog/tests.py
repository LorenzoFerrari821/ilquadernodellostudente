from django.urls import resolve,reverse
from django.test import TestCase
from django.test import RequestFactory
from.views import *
from django.contrib.auth.models import AnonymousUser,User


class TestUrls(TestCase):                                                                                               #Testiamo la correttezza del controller

    def test_itemlist_url(self):
        path = reverse('catalog:Itemlist')
        assert resolve(path).view_name == 'catalog:Itemlist'

    def test_details_url(self):
        path = reverse('catalog:Itemdetail',kwargs={'item_id': 1})
        assert resolve(path).view_name == 'catalog:Itemdetail'

    def test_search_url(self):
        path = reverse('catalog:Search')
        assert resolve(path).view_name == 'catalog:Search'



class TestAuthenticated(TestCase):                                                                                      #Controlliamo il comportamento delle views in caso di utenti registrati/visitatori
    fixtures = [
        'dumpdata',
    ]

    def test_itemlist_authenticated(self):
        path = reverse('catalog:Itemlist')
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = itemlist(request)
        assert response.status_code == 200

    def test_itemlist_unauthenticated(self):
        path = reverse('catalog:Itemlist')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = itemlist(request)
        assert response.status_code == 200

    def test_itemdetail_authenticated(self):
        path = reverse('catalog:Itemdetail', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = itemdetail(request,1)
        assert response.status_code == 200

    def test_itemdetails_unauthenticated(self):
        path = reverse('catalog:Itemdetail', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = itemdetail(request,1)
        assert response.status_code == 200

    def test_search_authenticated(self):
        path = reverse('catalog:Search')
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = search(request)
        assert response.status_code == 200

    def test_search_unauthenticated(self):
        path = reverse('catalog:Search')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = search(request)
        assert response.status_code == 200
