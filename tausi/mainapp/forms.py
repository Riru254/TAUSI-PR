from django import forms
from .models import Booking, BlogPost
from accounts.models import CustomUser

PACKAGE_CHOICES = [
    ('Luxury Safari', 'Luxury Safari'),
    ('Coastal Retreat', 'Coastal Retreat'),
    ('Mount Kenya Trek', 'Mount Kenya Trek'),
    ('Nairobi City Experience', 'Nairobi City Experience'),
    ('Amboseli Adventure', 'Amboseli Adventure'),
]


# forms.py
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'package', 'travel_date', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-select'}),
            'travel_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nationality', 'profile_pic']