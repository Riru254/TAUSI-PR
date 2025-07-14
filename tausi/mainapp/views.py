from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .forms import BookingForm, BlogPostForm, CustomUserUpdateForm
from .models import BlogPost
from accounts.models import COUNTRIES
from django.contrib.auth.decorators import login_required
from mainapp.models import Booking, Notification, SupportTicket
from datetime import date
from urllib.parse import urlencode
from django.template.loader import get_template
from xhtml2pdf import pisa


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
            booking = form.save(commit=False)
            booking.user = request.user  # This links the booking to the logged-in user
            booking.save()
            form.save()
            messages.success(request, "Your booking was successfully submitted!")
            Notification.objects.create(
                user=booking.user,
                message=f"✅ Your booking for {booking.package} is confirmed!"
                )
            return redirect('booking')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})

@login_required
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

@login_required
def dashboard_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserUpdateForm(instance=user)

    bookings = Booking.objects.filter(user=user).order_by('-booking_date')
    upcoming = bookings.filter(travel_date__gte=date.today())
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]

    return render(request, 'dashboard.html', {
        'user': user,
        'form': form,
        'bookings': bookings,
        'upcoming': upcoming,
        'notifications': notifications,
        'countries': COUNTRIES
    })


# Map package name to modal ID
PACKAGE_TO_MODAL = {
    'Luxury Safari': 'modalSafari',
    'Coastal Retreat': 'modalCoast',
    'Mount Kenya Trek': 'modalMountKenya',
    'Nairobi City Experience': 'modalNairobi',
    'Amboseli Adventure': 'modalAmboseli',
}
@login_required
def booking_detail_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    modal_id = PACKAGE_TO_MODAL.get(booking.package, '')
    query_string = urlencode({'modal': modal_id})
    return redirect(f'/packages/?{query_string}')

@login_required
def cancel_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.save()
        Notification.objects.create(
            user=booking.user,
            message=f"⚠️ Your booking for {booking.package} has been cancelled."
        )    
    return redirect('dashboard')

@login_required
def delete_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status == 'cancelled':
        Notification.objects.create(
            user=request.user,
            message=f"🗑️ Your cancelled booking for '{booking.package}' on {booking.travel_date} was permanently deleted."
        )
        booking.delete()
    return redirect('dashboard')

@login_required
def submit_support_ticket(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if subject and message:
            SupportTicket.objects.create(
                user=request.user,
                subject=subject,
                message=message
            )
            messages.success(request, "Your support request was submitted. We will get back to you!")
        else:
            messages.error(request, "Please fill in all fields.")
    return redirect('dashboard')

@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    return redirect('dashboard')
@login_required
def clear_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return redirect('dashboard')

@login_required
def download_invoice(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    template_path = 'invoice.html'
    context = {'booking': booking}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking.pk}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating invoice PDF', status=500)
    return response

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated.")
        else:
            messages.error(request, "Please correct the errors below.")
        return redirect('dashboard')  # or wherever your dashboard URL name is

    return redirect('dashboard')  # fallback

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Validate old password
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('dashboard')

        # Check new passwords match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('dashboard')

        # Set new password
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully.")
        return redirect('dashboard')

    return redirect('dashboard')


@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user

        if user.check_password(password):
            logout(request)
            user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('homepage') 
        else:
            messages.error(request, "Incorrect password. Account not deleted.")
            return redirect('dashboard')

    return redirect('dashboard')

