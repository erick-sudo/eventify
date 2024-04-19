from django.contrib import admin
from .models import Event, Booking

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ['name', 'desc']
#     search_fields = ['name', 'desc']

# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ['cus_name', 'cus_ph', 'name', 'booking_date', 'booked_on']
#     search_fields = ['cus_name', 'cus_ph']
#     list_filter = ['booking_date']
