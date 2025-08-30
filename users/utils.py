# Notification utility functions
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from notifications.models import Notification
# For WhatsApp/SMS (Twilio)
from twilio.rest import Client

def send_booking_confirmation(user, booking):
	subject = 'Booking Confirmation'
	message = f"Dear {user.name}, your booking for {booking.event.name} is confirmed. Ticket ID: {booking.id}"
	email = EmailMessage(subject, message, to=[user.email])
	status = 'sent'
	try:
		email.send()
	except Exception:
		status = 'failed'
	Notification.objects.create(user=user, notif_type='email', message=message, status=status)
	# WhatsApp/SMS
	send_whatsapp_message(user, message)

def send_event_reminder(user, event):
	subject = 'Event Reminder'
	message = f"Reminder: {event.name} starts on {event.start_time}. Don't miss it!"
	email = EmailMessage(subject, message, to=[user.email])
	status = 'sent'
	try:
		email.send()
	except Exception:
		status = 'failed'
	Notification.objects.create(user=user, notif_type='email', message=message, status=status)
	send_whatsapp_message(user, message)

def send_organizer_alert(user, event, alert_type):
	if alert_type == 'new_booking':
		message = f"A new booking has been made for your event: {event.name}."
	elif alert_type == 'sold_out':
		message = f"Tickets for your event {event.name} are sold out."
	else:
		message = f"Alert regarding your event: {event.name}."
	email = EmailMessage('Organizer Alert', message, to=[user.email])
	status = 'sent'
	try:
		email.send()
	except Exception:
		status = 'failed'
	Notification.objects.create(user=user, notif_type='email', message=message, status=status)
	send_whatsapp_message(user, message)

def send_whatsapp_message(user, message):
	# Twilio WhatsApp API integration
	try:
		client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
		client.messages.create(
			body=message,
			from_=settings.TWILIO_WHATSAPP_NUMBER,
			to=f"whatsapp:{user.phone}"
		)
		Notification.objects.create(user=user, notif_type='whatsapp', message=message, status='sent')
	except Exception:
		Notification.objects.create(user=user, notif_type='whatsapp', message=message, status='failed')
