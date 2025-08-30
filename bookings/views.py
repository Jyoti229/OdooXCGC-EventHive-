from .models import TicketInstance, CheckIn
def checkin_scan(request):
    message = None
    ticket_id = None
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        try:
            ticket = TicketInstance.objects.get(ticket_id=ticket_id)
            booking = ticket.booking
            checkin, created = CheckIn.objects.get_or_create(booking=booking)
            if checkin.status == 'checked_in':
                message = 'Ticket already checked in.'
            else:
                checkin.status = 'checked_in'
                from django.utils import timezone
                checkin.checkin_time = timezone.now()
                checkin.save()
                message = 'Check-in successful!'
        except TicketInstance.DoesNotExist:
            message = 'Invalid or unknown ticket.'
    return render(request, 'bookings/checkin_scan.html', {'message': message, 'ticket_id': ticket_id})
from django.shortcuts import render, get_object_or_404, redirect
from events.models import Event, TicketType
from .forms import BookingForm
from .models import Booking

def event_list(request):
    events = Event.objects.all()
    return render(request, "bookings/event_list.html", {"events": events})


def booking_form(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    ticket_types = TicketType.objects.filter(event=event)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        form.fields['event'].initial = event
        form.fields['ticket_type'].queryset = ticket_types
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.total_price = booking.ticket_type.price * booking.quantity
            booking.save()
            # Optionally: reduce ticket availability here
            return redirect('payment_confirm', booking_id=booking.id)
    else:
        form = BookingForm(initial={'event': event})
        form.fields['ticket_type'].queryset = ticket_types
    return render(request, 'bookings/booking_form.html', {'form': form, 'event': event})


def payment_confirm(request, booking_id):
    from .models import Payment, Booking, TicketInstance
    from .utils import generate_qr_code
    import uuid
    booking = get_object_or_404(Booking, pk=booking_id)
    # Mock payment: mark as paid
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'method': 'card',
            'status': 'success',
            'transaction_id': f'MOCK-{booking_id}',
            'amount': booking.total_price,
        }
    )
    booking.payment_status = 'success'
    booking.save()

    # Generate ticket and QR code
    ticket_id = str(uuid.uuid4())
    qr_filename = f"ticket_{ticket_id}.png"
    qr_path = generate_qr_code(ticket_id, qr_filename)
    ticket_instance, created = TicketInstance.objects.get_or_create(
        booking=booking,
        defaults={
            'ticket_id': ticket_id,
            'qr_code': qr_path,
        }
    )
    return render(request, 'bookings/payment_confirm.html', {'booking': booking, 'payment': payment, 'ticket_instance': ticket_instance})
