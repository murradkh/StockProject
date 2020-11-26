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
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/watchlist/', views.watchlist_view, name='watchlist'),
    path('accounts/portfolio/', views.portfolio_view, name='portfolio'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/password/', views.password_change_view, name='password_change'),
    path('accounts/register/', views.register, name='register'),
    path('notifications/', views.list_notifications_view, name='list_notifications'),
    path('notifications/unread_count/', views.notification_unread_count_view, name='notification_unread_count'),
    path('notifications/nread/', views.notifications_mark_read_view, name='notifications_all_read'),
    path('notifications/<int:pk>/nread/', views.notifications_mark_read_view, name='single_notification_read'),
    path('notifications/nremove/', views.notification_remove_view, name='clear_notifications'),
    path('notifications/<int:pk>/nremove/', views.notification_remove_view, name='single_notification_remove'),
    path('rules/<str:symbol>/', views.rules_list_view, name='stock_rules_list'),
    path('rules/add/<str:rule_type>/<str:symbol>/', views.add_rule_view, name='add_notification_rule'),
    path('rules/edit/<str:rule_type>/<int:pk>/', views.edit_rule_view, name='edit_notification_rule'),
    path('rules/delete/<str:rule_type>/<int:pk>/', views.delete_rule_view, name='delete_notification_rule'),
]
