from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Event, Booking
from django.contrib.auth.decorators import login_required

def index(request):
    latest_events = Event.objects.all().order_by('-date')[:6]
    return render(request, 'index.html', { 'events': latest_events })

def about(request):
    return render(request, 'about.html')

def events(request):
    event_list = Event.objects.all()
    paginator = Paginator(event_list, 6)  # Show 10 events per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'events.html', {'page_obj': page_obj})


@login_required(login_url="/user/login")
def bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings.html', {'bookings': bookings})

def cancel_booking(request, id):
    if Booking.objects.filter(id=id).exists():
        booking = Booking.objects.get(id=id)
        if request.method == 'POST':
            booking.delete()
    return redirect('/bookings')

@login_required(login_url="/user/login")
def book_event(request, id):
    state = None
    if Event.objects.filter(id=id).exists():
        event = Event.objects.get(id=id)
        if request.method == 'POST':
            if not Booking.objects.filter(event=event, user=request.user).exists():
                booking = Booking.objects.create(event=event, user=request.user)
                state = {
                    'posting': True,
                    'success': True,
                    'message': 'Your have successfully booked a slot for this event.',
                    'event': event
                }
            else:
                state = {
                    'posting': True,
                    'success': False,
                    'message': "You already have a slot for this event",
                    'event': event
                }
        else:
            state = {
                'success': True,
                'event': event
            }
    else:
        state = {
            'success': False,
            'message': 'Event does not exist.',
            'event': None
        }
    return render(request, 'book_event.html', {'booking_state': state})

def about(request):
    return render(request, 'about.html')

