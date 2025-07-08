from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .forms import BookingForm, BlogPostForm
from .models import BlogPost


# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def packages(request):
    return render(request, 'packages.html')

def confirmation(request):
    return render(request, 'confirmation.html')


def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    return render(request, 'register.html')

def homepage_view(request):
    return render(request, 'homepage.html')


form = BookingForm()
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your booking was successfully submitted!")
            return redirect('booking')  # Adjust if your booking page has a different name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})


def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'create_blog_post.html', {'form': form})