from django.db import models
from django.conf import settings
from datetime import date
from accounts.models import CustomUser
from django import forms

class Booking(models.Model):
    PACKAGE_CHOICES = [
        ('Luxury Safari', 'Luxury Safari'),
        ('Coastal Retreat', 'Coastal Retreat'),
        ('Mount Kenya Trek', 'Mount Kenya Trek'),
        ('Nairobi City Experience', 'Nairobi City Experience'),
        ('Amboseli Adventure', 'Amboseli Adventure'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    package = models.CharField(max_length=50, choices=PACKAGE_CHOICES)
    travel_date = models.DateField()
    notes = models.TextField(blank=True)
    booking_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('cancelled', 'Cancelled')], default= 'pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def is_upcoming(self):
        return self.travel_date >= date.today()
    
    def __str__(self):
        return f"{self.name} - {self.package}"

class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message[:40]}"
    
class SupportTicket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], default='open')

    def __str__(self):
        return f"{self.user.username} - {self.subject[:30]}"

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nationality', 'profile_pic']