from django.contrib import admin
from .models import Booking, Notification, SupportTicket

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'package', 'travel_date', 'status', 'booking_date')
    list_filter = ('status', 'package')
    search_fields = ('name', 'email', 'package')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    search_fields = ('message', 'user__username')

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'submitted_at', 'status')
    list_filter = ('status',)
    search_fields = ('subject', 'message', 'user__username')

