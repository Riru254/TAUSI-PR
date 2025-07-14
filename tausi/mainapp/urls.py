from django.urls import path
from . import views
from .views import delete_account, create_blog_post, dashboard_view, booking_detail_view, cancel_booking_view, delete_booking_view, delete_notification,clear_all_notifications, download_invoice, update_profile_view, change_password


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('homepage/', views.homepage, name='homepage'),
    path('booking/', views.booking_view, name='booking'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('packages/', views.packages, name='packages'),
    path('blog/create/', views.create_blog_post, name='create_blog'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('booking/<int:pk>/view/', views.booking_detail_view, name='booking_detail'),
    path('booking/<int:pk>/cancel/', views.cancel_booking_view, name='cancel_booking'),
    path('booking/<int:pk>/delete/', views.delete_booking_view, name='delete_booking'),
    path('notification/<int:pk>/delete/', views.delete_notification, name='delete_notification'),
    path('notifications/clear/', views.clear_all_notifications, name='clear_all_notifications'),
    path('booking/<int:pk>/invoice/', views.download_invoice, name='download_invoice'),
    path('support/submit/', views.submit_support_ticket, name='submit_support_ticket'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('password/change/', views.change_password, name='change_password'),
    path('account/delete/', views.delete_account, name='delete_account'),


]