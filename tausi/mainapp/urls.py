from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('homepage/', views.homepage, name='homepage'),
    path('booking/', views.booking_view, name='booking'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('packages/', views.packages, name='packages'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('booking/<int:pk>/view/', views.booking_detail_view, name='booking_detail'),
    path('booking/<int:pk>/cancel/', views.cancel_booking_view, name='cancel_booking'),
    path('booking/<int:pk>/delete/', views.delete_booking_view, name='delete_booking'),
    path('notification/<int:pk>/delete/', views.delete_notification, name='delete_notification'),
    path('notifications/clear/', views.clear_all_notifications, name='clear_all_notifications'),
    path('booking/<int:pk>/invoice/', views.generate_invoice, name='download_invoice'),
    path('support/submit/', views.submit_support_ticket, name='submit_support_ticket'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('password/change/', views.change_password, name='change_password'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('toggle-like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('blogs/', views.blog_list_view, name='blog-list'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('delete-blog/<int:post_id>/', views.delete_blog, name='delete_blog'),
    path('my-blogs/', views.user_blogs, name='user_blogs'),
    path('blogs/add/', views.add_blog, name='add_blog'),
    path('booking/<int:pk>/invoice/', views.generate_invoice, name='download_invoice'),





]