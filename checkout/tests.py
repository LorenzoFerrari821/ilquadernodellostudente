from django.urls import resolve
from django.test import TestCase
from django.test import RequestFactory
from.views import *
from django.contrib.auth.models import AnonymousUser,User


class TestUrls(TestCase):                                                                                               #Testiamo la correttezza del controller

    def test_Cart_url(self):
        path = reverse('checkout:Cart')
        assert resolve(path).view_name == 'checkout:Cart'

    def test_additem_url(self):
        path = reverse('checkout:Additem',kwargs={'item_id': 1})
        assert resolve(path).view_name == 'checkout:Additem'

    def test_deleteitem_url(self):
        path = reverse('checkout:Deleteitem', kwargs={'item_id': 1})
        assert resolve(path).view_name == 'checkout:Deleteitem'

    def test_payment_url(self):
        path = reverse('checkout:Payment', kwargs={'cart_id': 1})
        assert resolve(path).view_name == 'checkout:Payment'

    def test_retrieve_url(self):
        path = reverse('checkout:Retrieve', kwargs={'item_id': 1})
        assert resolve(path).view_name == 'checkout:Retrieve'

    def test_placeorder_url(self):
        path = reverse('checkout:Placeorder', kwargs={'cart_id': 1})
        assert resolve(path).view_name == 'checkout:Placeorder'



class TestAuthenticated(TestCase):                                                                                      #Controlliamo il comportamento delle views in caso di utenti registrati/visitatori
    fixtures = [
        'dumpdata',
    ]

    def test_cart_authenticated(self):
        path = reverse('checkout:Cart')
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = cart(request)
        assert response.status_code == 200

    def test_cart_unauthenticated(self):
        path = reverse('checkout:Cart')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = cart(request)
        assert response.status_code == 302

    def test_additem_authenticated(self):
        path = reverse('checkout:Additem', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = additem(request,1)
        assert response.status_code == 200

    def test_additems_unauthenticated(self):
        path = reverse('checkout:Additem', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = additem(request,1)
        assert response.status_code == 302

    def test_deleteitem_authenticated(self):
        path = reverse('checkout:Deleteitem', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = deleteitem(request,1)
        assert response.status_code == 302

    def test_deleteitem_unauthenticated(self):
        path = reverse('checkout:Deleteitem', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = deleteitem(request, 1)
        assert response.status_code == 302

    def test_payment_authenticated(self):
        path = reverse('checkout:Payment', kwargs={'cart_id': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = payment(request, 1)
        assert response.status_code == 302

    def test_payment_unauthenticated(self):
        path = reverse('checkout:Payment', kwargs={'cart_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = payment(request, 1)
        assert response.status_code == 302

    def test_retrieve_authenticated(self):
        path = reverse('checkout:Retrieve', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = retrieve(request, 1)
        assert response.status_code == 200

    def test_retrieve_unauthenticated(self):
        path = reverse('checkout:Retrieve', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = retrieve(request, 1)
        assert response.status_code == 302

    def test_placeorder_authenticated(self):
        path = reverse('checkout:Placeorder', kwargs={'cart_id': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = placeorder(request, 1)
        assert response.status_code == 200

    def test_placeorder_unauthenticated(self):
        path = reverse('checkout:Placeorder', kwargs={'cart_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = placeorder(request, 1)
        assert response.status_code == 302
