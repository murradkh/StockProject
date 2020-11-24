from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/<str:symbol>/', views.single_stock, name='single_stock'),
    path('historic/<str:symbols>/', views.single_stock_historic, name='single_stock_historic'),
    path('historic/<str:symbols>/<str:time_range>/', views.single_stock_historic, name='single_stock_range'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/watchlist/', views.watchlist_view, name='watchlist'),
    path('accounts/portfolio/', views.portfolio_view, name='portfolio'),
    path('stock/<str:symbol>/wremove/', views.watchlist_remove_view, name='watchlist_remove'),
    path('stock/<str:symbol>/wadd/', views.watchlist_add_view, name='watchlist_add'),
    path('stock/<str:symbol>/buy/', views.buy_stock_view, name='buy_stock'),
    path('stock/<int:buy_id>/sell/', views.sell_stock_view, name='sell_stock'),
    path('stocks/list_names/<str:search_text>', views.list_stocks_names_view, name='list_stocks_names'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/password/', views.password_change_view, name='password_change'),
    path('accounts/register/', views.register, name='register'),

]
