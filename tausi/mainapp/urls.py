from django.urls import path
from . import views
from .views import create_blog_post


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('homepage/', views.homepage, name='homepage'),
    path('booking/', views.booking_view, name='booking'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('packages/', views.packages, name='packages'),
    path('blog/create/', create_blog_post, name='create_blog'),
]