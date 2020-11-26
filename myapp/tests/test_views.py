from django.contrib.auth.models import User
from django.test import Client
from myapp.models import Profile, Stock, Notification
from django.test import TestCase


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='tester',
                                                  password='randomexample')
        self.client.post('/accounts/login/', {'username': 'tester', 
                                              'password': 'randomexample'})

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
        response = self.client.get(
            "/historic/{symbols}/".format(symbols=",".join(self.existed_symbols + self.not_existed_symbols)))
        self.assertContains(response, "data")
        response_json = response.json()['data']
        self.assertEquals(len(response_json), len(self.existed_symbols))
        response = self.client.get(
            "/historic/{symbols}/".format(symbols="," + self.existed_symbols[0] + ","))
        self.assertContains(response, "data")
        response_json = response.json()['data']
        self.assertIsInstance(response_json, list)

    def test_list_stocks_names_view(self):
        response = self.client.get("/stocks/list_names/snap-mm")
        self.assertContains(response, 'stocks_names')
        self.assertEqual(len(response.json()['stocks_names']), 1)
        response = self.client.get("/stocks/list_names/ ")
        self.assertContains(response, 'stocks_names')
        self.assertEqual(len(response.json()['stocks_names']), 0)
        response = self.client.get("/stocks/list_names/")
        self.assertEquals(response.status_code, 404)


class NotificationsViewTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='tester',
                                                  password='randomexample')

        self.test_stock_1 = Stock.objects.create(symbol="APPL",
                                                name='Apple',
                                                top_rank=1,
                                                price=10.0, 
                                                change=2.0, 
                                                change_percent=20.0)

        self.test_notif_1 = Notification.objects.create(title="Apple Notification 1",
                                                        description="First Apple notification",
                                                        stock=self.test_stock_1, 
                                                        user=Profile.objects.get(user=self.test_user))

        self.test_notif_2 = Notification.objects.create(title="Apple Notification 2",
                                                        description="Second Apple notification",
                                                        stock=self.test_stock_1, 
                                                        user=Profile.objects.get(user=self.test_user))

        self.client.post('/accounts/login/', {'username': 'tester', 
                                              'password': 'randomexample'})


    def test_notifications_list(self):
        response = self.client.get("/notifications/")
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(len(response.json()), 2)

    def test_notifications_all_unread(self):
        response = self.client.get("/notifications/")
        for key in response.json():
            self.assertFalse(response.json()[key]['is_read'])
        response = self.client.get("/notifications/unread_count/")
        self.assertEqual(response.json()['unread_count'], 2)

    def test_notifications_one_read(self):
        self.client.post(f"/notifications/{self.test_notif_1.pk}/nread/")
        response = self.client.get("/notifications/")
        self.assertTrue(response.json()[str(self.test_notif_1.pk)]['is_read'])
        self.assertFalse(response.json()[str(self.test_notif_2.pk)]['is_read'])
        response = self.client.get("/notifications/unread_count/")
        self.assertEqual(response.json()['unread_count'], 1)
    
    def test_notifications_all_read(self):
        self.client.post("/notifications/nread/")
        response = self.client.get("/notifications/")
        for key in response.json():
            self.assertTrue(response.json()[key]['is_read'])
        response = self.client.get("/notifications/unread_count/")
        self.assertEqual(response.json()['unread_count'], 0)
    
    def test_notifications_delete_one(self):
        id_1 = self.test_notif_1.pk
        self.client.post(f"/notifications/{id_1}/nremove/")
        response = self.client.get("/notifications/")
        self.assertRaises(KeyError, lambda: response.json()[str(id_1)]['title'])   # no longer exists in dict
        self.assertEqual(len(response.json()), 1)

    def test_notifications_clear_all(self):
        self.client.post("/notifications/nremove/")
        response = self.client.get("/notifications/")
        self.assertEqual(len(response.json()), 0)
