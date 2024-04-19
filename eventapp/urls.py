from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),  # Add this line
    path('events', views.events, name='events'),
    path('bookings', views.bookings, name='bookings'),
    path('events/<id>', views.book_event, name='book_event'),
    path('bookings/<id>/cancel', views.cancel_booking, name='cancel_booking')
]
