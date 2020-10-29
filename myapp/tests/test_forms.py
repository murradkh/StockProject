from django.contrib.auth.models import User
from django.test import TestCase
from myapp.forms import CustomRegistrationFrom, CustomChangePasswordForm


class RegistrationFormTestCase(TestCase):
    def test_normal_registration(self):
        test_data = {'username': 'tester@gmail.com',
                    'password1': 'randomexample',
                    'password2': 'randomexample'}
        form = CustomRegistrationFrom(data=test_data)
        self.assertTrue(form.is_valid())

    def test_username_not_email(self):
        test_data = {'username': 'testuser',
                    'password1': 'randomexample',
                    'password2': 'randomexample'}
        form = CustomRegistrationFrom(data=test_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors.keys())

    def test_passwords_dont_match(self):
        test_data = {'username': 'tester@gmail.com',
                    'password1': 'randomexample',
                    'password2': 'randomezzampl'}
        form = CustomRegistrationFrom(data=test_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors.keys())

    def test_username_already_taken(self):
        test_user = User.objects.create_user(username='tester@gmail.com',
                                            password='firstuser123')
        test_data = {'username': 'tester@gmail.com',
                    'password1': 'randomexample',
                    'password2': 'randomexample'}
        form = CustomRegistrationFrom(data=test_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors.keys())


class ChangePasswordFormTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='tester@gmail.com',
                                                password='firstuser123')

    def test_normal_password_change(self):
        test_data = {'old_password': 'firstuser123',
                    'new_password1': 'randomexample',
                    'new_password2': 'randomexample'}
        form = CustomChangePasswordForm(self.test_user, data=test_data)
        self.assertTrue(form.is_valid())

    def test_wrong_old_password(self):
        test_data = {'old_password': 'wrongpass123',
                    'new_password1': 'randomexample',
                    'new_password2': 'randomexample'}
        form = CustomChangePasswordForm(self.test_user, data=test_data)
        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors.keys())

    def test_empty_new_password(self):
        test_data = {'old_password': 'firstuser123',
                    'new_password1': '',
                    'new_password2': ''}
        form = CustomChangePasswordForm(self.test_user, data=test_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password1', form.errors.keys())

    def test_new_passwords_dont_match(self):
        test_data = {'old_password': 'firstuser123',
                    'new_password1': 'randomexample',
                    'new_password2': 'randomezzampl'}
        form = CustomChangePasswordForm(self.test_user, data=test_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors.keys())
