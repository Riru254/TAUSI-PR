from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from accounts.models import CustomUser
from .forms import LoginForm,CustomRegisterForm
from django.contrib.auth import logout
from mainapp.models import Booking

def tausi_logout_view(request):
    print("LOGOUT VIEW HIT")
    logout(request) #Clears the session
    messages.info(request, "You’ve logged out. Come back soon 🌿")
    return redirect('/')


def login_view(request):
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = CustomUser.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.username}!")
                    
                    # ✅ Redirect staff users to Django admin
                    if user.is_staff:
                        return redirect('/admin/')
                    
                    # Regular users
                    return redirect('homepage')
                else:
                    messages.error(request, "Incorrect password.")
            except CustomUser.DoesNotExist:
                messages.error(request, "No account found with that email.")
        else:
            messages.error(request, "Please correct the form errors.")
    
    return render(request, 'login.html', {'form': form})


def register_view(request):
    form = CustomRegisterForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('homepage')
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    return render(request, 'dashboard.html', {
        'user': user,
        'bookings': bookings,
    })