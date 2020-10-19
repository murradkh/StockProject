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
	path('accounts/watchlist/', views.watchlist_view, name='watchlist'),
	path('stock/<str:symbol>/<str:operation>/', views.watchlist_edit_view, name='watchlist_edit'),
	path('accounts/profile/', views.profile_view, name='profile'),
	path('accounts/password/', views.password_change_view, name='password_change'),
	path('accounts/register/', views.register, name='register'),
]
