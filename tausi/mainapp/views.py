from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .forms import BookingForm, BlogPostForm, CustomUserUpdateForm, CommentForm, InquiryForm
from .models import BlogPost, Comment
from accounts.models import COUNTRIES
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from mainapp.models import Booking, Notification, SupportTicket, Invoice
from datetime import date, timedelta
from urllib.parse import urlencode
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.paginator import Paginator

# Create your views here.
def homepage(request):
    blogs = BlogPost.objects.all().order_by('-created_at')[:3]
    return render(request, 'homepage.html',{'blogs': blogs})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message was sent successfully!")
            return redirect('contact')  # Replace 'contact' with your URL name if different
    else:
        form = InquiryForm()
    
    return render(request, 'contact.html', {'form': form})

def packages(request):
    return render(request, 'packages.html')

def confirmation(request):
    return render(request, 'confirmation.html')


def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    return render(request, 'register.html')
from django.core.paginator import Paginator

def blog_list_view(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(blogs, 2)  # 6 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj,
                                         'blogs': blogs})

#def homepage_view(request):
    return render(request, 'homepage.html')


form = BookingForm()
@login_required
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
def dashboard_view(request):
    blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')[:3]
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
        'countries': COUNTRIES,
        "blogs": blogs
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
def generate_invoice(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    def calculate_amount(booking):
        package_prices = {
            'Luxury Safari': 22500,
            'Coastal Retreat': 17500,
            'Mount Kenya Trek': 12500,
            'Nairobi City Experience': 7500,
            'Amboseli Adventure': 35000,
        }
        return package_prices.get(booking.package, 1000)
    # If invoice already exists
    if hasattr(booking, 'invoice'):
        invoice = booking.invoice
    else:
        # Create new invoice
        invoice = Invoice.objects.create(
            booking=booking,
            due_date=date.today() + timedelta(days=7),
            amount=calculate_amount(booking),  # You define this logic
        )

    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})

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

@login_required
def add_blog(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect('add_blog')  
    return render(request, 'blogs/add_blog.html', {'form': form})

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    liked = False

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': post.likes.count(),
    })

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        blog = get_object_or_404(BlogPost, id=post_id)
        content = request.POST.get("comment")
        if content:
            Comment.objects.create(blog=blog, author=request.user, content=content)
            messages.success(request, "Comment added successfully.")
        else:
            messages.warning(request, "Comment cannot be empty.")
    return redirect('blog_detail', post_id=post_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blogs/blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def user_blogs(request):
    user_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(user_posts, 3) # Second argument- x blogs per page
    page_number = request.GET.get('page') # Very important
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs/user_blogs.html', {'page_obj': page_obj})

@login_required
def delete_blog(request, post_id):
    blog = get_object_or_404(BlogPost, id=post_id, author=request.user)
    blog.delete()
    return redirect('user_blogs')