from django.urls import resolve
from django.test import TestCase
from django.test import RequestFactory
from.views import *
from django.contrib.auth.models import AnonymousUser


class TestUrls(TestCase):                                                                                               #Testiamo la correttezza del controller

    def test_login_url(self):
        path = reverse('users:Login')
        assert resolve(path).view_name == 'users:Login'

    def test_signup_url(self):
        path = reverse('users:Signup')
        assert resolve(path).view_name == 'users:Signup'

    def test_logout_url(self):
        path = reverse('users:Logout')
        assert resolve(path).view_name == 'users:Logout'

    def test_profile_url(self):
        path = reverse('users:Profile', kwargs={'user_id': 1})
        assert resolve(path).view_name == 'users:Profile'

    def test_editimage_url(self):
        path = reverse('users:Editimage')
        assert resolve(path).view_name == 'users:Editimage'

    def test_editdata_url(self):
        path = reverse('users:Editdata')
        assert resolve(path).view_name == 'users:Editdata'

    def test_editpassword_url(self):
        path = reverse('users:Editpassword')
        assert resolve(path).view_name == 'users:Editpassword'

    def test_purchaselist_url(self):
        path = reverse('users:Purchaselist')
        assert resolve(path).view_name == 'users:Purchaselist'

    def test_create_url(self):
        path = reverse('users:Create')
        assert resolve(path).view_name == 'users:Create'

    def test_selectitem_url(self):
        path = reverse('users:Selectitem')
        assert resolve(path).view_name == 'users:Selectitem'

    def test_deleteitem_url(self):
        path = reverse('users:Deleteitem',kwargs={'item_id': 1})
        assert resolve(path).view_name == 'users:Deleteitem'

    def test_edititem_url(self):
        path = reverse('users:Edititem',kwargs={'item_id': 1})
        assert resolve(path).view_name == 'users:Edititem'

    def test_review_url(self):
        path = reverse('users:Review',kwargs={'item_id': 1})
        assert resolve(path).view_name == 'users:Review'


class TestAuthenticated(TestCase):                                                                                      #Controlliamo il comportamento delle views in caso di utenti registrati/visitatori
    fixtures = [
        'dumpdata',
    ]

    def test_editimage_authenticated(self):
        path = reverse('users:Editimage')
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = editimage(request)
        assert response.status_code == 200

    def test_editimage_unauthenticated(self):
        path = reverse('users:Editimage')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = editimage(request)
        assert response.status_code == 302

    def test_editdata_authenticated(self):
        path = reverse('users:Editdata')
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = editdata(request)
        assert response.status_code == 200

    def test_editdata_unauthenticated(self):
        path = reverse('users:Editdata')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = editdata(request)
        assert response.status_code == 302

    def test_editpassword_authenticated(self):
        path = reverse('users:Editpassword')
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = editpassword(request)
        assert response.status_code == 200

    def test_editpassword_unauthenticated(self):
        path = reverse('users:Editpassword')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = editpassword(request)
        assert response.status_code == 302

    def test_purchaselist_authenticated(self):
        path = reverse('users:Purchaselist')
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = purchaselist(request)
        assert response.status_code == 200

    def test_purchaselist_unauthenticated(self):
        path = reverse('users:Purchaselist')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = purchaselist(request)
        assert response.status_code == 302

    def test_create_authenticated(self):
        path = reverse('users:Create')
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = create(request)
        assert response.status_code == 200

    def test_create_unauthenticated(self):
        path = reverse('users:Create')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = create(request)
        assert response.status_code == 302

    def test_selectitem_authenticated(self):
        path = reverse('users:Selectitem')
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = selectitem(request)
        assert response.status_code == 200

    def test_selectitem_unauthenticated(self):
        path = reverse('users:Selectitem')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = selectitem(request)
        assert response.status_code == 302

    def test_deleteitem_authenticated(self):
        path = reverse('users:Deleteitem', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = deleteitem(request, 1)
        assert response.status_code == 200

    def test_deleteitem_unauthenticated(self):
        path = reverse('users:Deleteitem', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = deleteitem(request, 1)
        assert response.status_code == 302

    def test_edititem_authenticated(self):
        path = reverse('users:Edititem', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = edititem(request, 1)
        assert response.status_code == 200

    def test_edititem_unauthenticated(self):
        path = reverse('users:Edititem', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = edititem(request, 1)
        assert response.status_code == 302

    def test_review_authenticated(self):
        path = reverse('users:Review', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = User.objects.get(username='admin')
        self.client.login(username='admin', password='admin')
        response = review(request, 1)
        assert response.status_code == 200

    def test_review_unauthenticated(self):
        path = reverse('users:Review', kwargs={'item_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = review(request, 1)
        assert response.status_code == 302






