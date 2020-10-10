from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/<str:symbol>/', views.single_stock, name='single_stock'),
    path('historic/<str:symbol>/', views.single_stock_historic, name='single_stock_historic'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    re_path("", views.page_not_found, name='page_not_found'),

]
