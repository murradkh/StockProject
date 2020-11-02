from django.contrib.auth.models import User
from django.test import Client, TestCase
from myapp.models import Profile, Stock


class StockWatchlistTestCase(TestCase):
    def setUp(self):
        self.test_stock = Stock.objects.create(symbol="APPL", name='Apple', top_rank=1, price=10.0, change=1.0, change_percent=15.0)
        
        self.test_user_1 = User.objects.create_user(username='tester1', password='randomexample')
        self.test_user_2 = User.objects.create_user(username='tester2', password='secondpass468')
        
        self.client = Client()
        self.client.post('/accounts/login/', {'username': 'tester1', 'password': 'randomexample'})

    def test_watchlist_add(self):
        self.client.post('/stock/APPL/wadd/') 
        self.assertIn(self.test_stock, Profile.objects.get(user=self.test_user_1).watchlist.all())
        self.assertTrue(Stock.is_needed('APPL'))

    def test_watchlist_remove(self):
        self.client.post('/stock/APPL/wremove/')
        self.assertNotIn(self.test_stock, Profile.objects.get(user=self.test_user_1).watchlist.all())
        self.assertFalse(Stock.is_needed('APPL'))

    def test_watchlist_add_non_existant(self):
        response = self.client.post('/stock/GE/wadd/')
        self.assertEqual(response.status_code, 404)    # 404 since stock not in db
        self.assertEqual(Profile.objects.get(user=self.test_user_1).watchlist.all().count(), 0)
        self.assertFalse(Stock.is_needed('GE'))

    def test_watchlist_add_unauthenticated(self):
        self.client.logout()
        response = self.client.post('/stock/APPL/wadd/')    # Must redirect to login page
        self.assertRedirects(response, '/accounts/login/?next=/stock/APPL/wadd/')

    def test_stock_is_needed(self):
        self.client.post('/accounts/login/', {'username': 'tester1', 'password': 'randomexample'})
        self.client.post('/stock/APPL/wadd/')
        self.client.logout()
        self.client.post('/accounts/login/', {'username': 'tester2', 'password': 'secondpass468'})
        self.client.post('/stock/APPL/wremove/')
        self.assertTrue(Stock.is_needed('APPL'))    # stock still needed for tester1

    def test_watchlist_stock_deleted(self):
        self.client.post('/accounts/login/', {'username': 'tester1', 'password': 'randomexample'})
        self.client.post('/stock/APPL/wadd/')
        self.test_stock.delete()    # Deleted stock also removed from watchlist
        self.assertEqual(Profile.objects.get(user=self.test_user_1).watchlist.all().count(), 0)
        self.assertFalse(Stock.is_needed('APPL'))
