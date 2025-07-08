from django.db import models
from django.conf import settings

class Booking(models.Model):
    PACKAGE_CHOICES = [
        ('Luxury Safari', 'Luxury Safari'),
        ('Coastal Retreat', 'Coastal Retreat'),
        ('Mount Kenya Trek', 'Mount Kenya Trek'),
        ('Nairobi City Experience', 'Nairobi City Experience'),
        ('Amboseli Adventure', 'Amboseli Adventure'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null= True, blank= True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    package = models.CharField(max_length=50, choices=PACKAGE_CHOICES)
    date = models.DateField()
    notes = models.TextField(blank=True)

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