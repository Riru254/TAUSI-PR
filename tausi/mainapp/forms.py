from django import forms
from .models import Booking, BlogPost, Comment, Inquiry
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
        fields = [ 'email', 'phone', 'package', 'travel_date', 'notes']
        widgets = {
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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['fullname', 'email', 'subject', 'message']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'johndoe@gmail.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Message'}),
        }