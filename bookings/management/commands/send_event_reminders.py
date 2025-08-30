from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from bookings.models import Booking
from events.models import Event

class Command(BaseCommand):
    help = 'Send reminder emails to attendees for events happening tomorrow.'

    def handle(self, *args, **options):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        events = Event.objects.filter(date=tomorrow)
        for event in events:
            bookings = Booking.objects.filter(event=event, payment_status='success')
            for booking in bookings:
                subject = f'Reminder: {event.title} is tomorrow!'
                message = f'Dear {booking.user.username},\n\nThis is a reminder that {event.title} is happening tomorrow.\n\nDate: {event.date}\nLocation: {event.location}\n\nSee you there!\nEventHive Team'
                send_mail(subject, message, 'noreply@eventhive.com', [booking.user.email], fail_silently=True)
                self.stdout.write(self.style.SUCCESS(f'Reminder sent to {booking.user.email} for event {event.title}'))
