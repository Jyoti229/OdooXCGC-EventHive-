from django.contrib.auth.decorators import login_required
# Organizer Dashboard View
@login_required
def organizer_dashboard(request):
    # Get events organized by the current user
    from events.models import Event
    events = Event.objects.filter(organizer=request.user)
    # Get bookings for these events
    from .models import Booking
    event_stats = []
    for event in events:
        bookings = Booking.objects.filter(event=event, payment_status='success')
        total_tickets = sum(b.quantity for b in bookings)
        total_sales = sum(b.total_price for b in bookings)
        event_stats.append({
            'event': event,
            'total_tickets': total_tickets,
            'total_sales': total_sales,
            'bookings': bookings,
        })
    return render(request, 'bookings/organizer_dashboard.html', {'event_stats': event_stats})
from .models import TicketInstance, CheckIn
from django.shortcuts import render, get_object_or_404, redirect
from events.models import Event, TicketType
from .forms import BookingForm
from .models import Booking
from django.db import models
from django.core.mail import send_mail

def event_list(request):
    events = Event.objects.all()
    return render(request, "bookings/event_list.html", {"events": events})


def booking_form(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    ticket_types = TicketType.objects.filter(event=event)
    # Calculate remaining tickets for each type
    for tt in ticket_types:
        booked = Booking.objects.filter(event=event, ticket_type=tt, payment_status='success').aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        tt.remaining_quantity = tt.max_quantity - booked
    if request.method == 'POST':
        form = BookingForm(request.POST)
        form.fields['event'].initial = event
        form.fields['ticket_type'].queryset = ticket_types
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.total_price = booking.ticket_type.price * booking.quantity
            # Check remaining quantity before saving
            booked = Booking.objects.filter(event=event, ticket_type=booking.ticket_type, payment_status='success').aggregate(models.Sum('quantity'))['quantity__sum'] or 0
            remaining = booking.ticket_type.max_quantity - booked
            if booking.quantity > remaining:
                form.add_error('quantity', 'Not enough tickets available.')
                return render(request, 'bookings/booking_form.html', {'form': form, 'event': event, 'ticket_types': ticket_types})
            booking.save()
            # Notify organizer
            organizer = booking.event.organizer if hasattr(booking.event, 'organizer') else None
            if organizer and organizer.email:
                subject = f"New Booking for {booking.event.title}"
                message = f"A new booking has been made for your event {booking.event.title}.\n\nUser: {booking.user.username}\nTicket Type: {booking.ticket_type.name}\nQuantity: {booking.quantity}\nTotal Price: ₹{booking.total_price}"
                from django.core.mail import send_mail
                send_mail(subject, message, 'noreply@eventhive.com', [organizer.email], fail_silently=True)
            return redirect('payment_confirm', booking_id=booking.id)
    else:
        form = BookingForm(initial={'event': event})
        form.fields['ticket_type'].queryset = ticket_types
    return render(request, 'bookings/booking_form.html', {'form': form, 'event': event, 'ticket_types': ticket_types})


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

    # Send booking confirmation email
    subject = f"Booking Confirmation for {booking.event.title}"
    message = f"Dear {booking.user.username},\n\nYour booking for {booking.event.title} is confirmed!\n\nDetails:\nEvent: {booking.event.title}\nDate: {booking.event.date}\nLocation: {booking.event.location}\nTicket Type: {booking.ticket_type.name}\nQuantity: {booking.quantity}\nTotal Price: ₹{booking.total_price}\n\nThank you for booking with EventHive!"
    recipient = [booking.user.email]
    send_mail(subject, message, 'noreply@eventhive.com', recipient, fail_silently=True)

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

    # Render invoice as HTML and send as email
    from django.template.loader import render_to_string
    invoice_html = render_to_string('invoice.html', {'booking': booking})
    send_mail(
        f"Invoice for Booking #{booking.id}",
        "Please find your invoice attached.",
        'noreply@eventhive.com',
        [booking.user.email],
        html_message=invoice_html,
        fail_silently=True
    )

    return render(request, 'bookings/payment_confirm.html', {'booking': booking, 'payment': payment, 'ticket_instance': ticket_instance})


def checkin_scan(request):
    message = None
    ticket_id = None
    attendee = None
    booking = None
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        try:
            ticket = TicketInstance.objects.get(ticket_id=ticket_id)
            booking = ticket.booking
            attendee = booking.user
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
    return render(request, 'bookings/checkin_scan.html', {'message': message, 'ticket_id': ticket_id, 'attendee': attendee, 'booking': booking})