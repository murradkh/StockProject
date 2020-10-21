from django.contrib.auth.models import User
from django.test import Client, TestCase
from myapp.models import Profile


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
        response = self.client.get('/accounts/password/')   # Must redirect to login page
        self.assertRedirects(response, '/accounts/login/?next=/accounts/password/')
        self.assertTemplateNotUsed(response, template_name='password_change.html')
