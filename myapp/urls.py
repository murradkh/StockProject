from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('stock/<str:symbol>/', views.single_stock, name='single_stock'),
	path('historic/<str:symbol>/', views.single_stock_historic, name='single_stock_historic'),
	path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('accounts/logout/', views.logout_view, name='logout'),
	path('stock/watchlist', views.watchlist_view, name='watchlist'),
	path('stock/<str:symbol>/wremove', views.watchlist_remove_view, name='watchlist_remove'),
	path('stock/<str:symbol>/wadd', views.watchlist_add_view, name='watchlist_add'),
	path('accounts/me/', views.profile_view, name='profile'),
	path('accounts/register/', views.register, name='register'),
]
