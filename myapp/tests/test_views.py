from django.contrib.auth.models import User
from django.test import Client

from django.test import TestCase


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='tester', password='randomexample')
        self.client = Client()
        self.client.post('/accounts/login/', {'username': 'tester', 'password': 'randomexample'})

    def test_user_auth_profile(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='profile.html')

    def test_user_auth_watchlist(self):
        response = self.client.get('/accounts/watchlist/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='watchlist.html')

    def test_login_required_redirect(self):
        self.client.logout()
        response = self.client.get('/accounts/password/')  # Must redirect to login page
        self.assertRedirects(response, '/accounts/login/?next=/accounts/password/')
        self.assertTemplateNotUsed(response, template_name='password_change.html')


class EndPointsTestCase(TestCase):

    def setUp(self):
        self.existed_symbols = ['AAL', 'WFC', "CCL"]
        self.not_existed_symbols = ['kamal', 'murad', 'malak']

    def test_single_stock(self):
        for symbol in self.existed_symbols:
            response = self.client.get(f"/stock/{symbol}/")
            self.assertTemplateUsed(response, "single_stock.html")
            self.assertEquals(response.status_code, 200)
        for symbol in self.not_existed_symbols:
            response = self.client.get(f"/stock/{symbol}/")
            self.assertTemplateUsed(response, "exception.html")
            self.assertEquals(response.status_code, 404)

    def test_single_stock_historic(self):
        for symbol in self.existed_symbols:
            response = self.client.get(f"/historic/{symbol}/")
            self.assertContains(response, "data")
        for symbol in self.not_existed_symbols:
            response = self.client.get(f"/historic/{symbol}/")
            self.assertContains(response, "error_message", status_code=404)
