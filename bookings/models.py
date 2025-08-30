from django.db import models
from django.conf import settings 
from events.models import Event, TicketType 

class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.event.title}"

class Payment(models.Model):
    METHOD_CHOICES = [
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('cash', 'Cash'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id} - {self.status}"

class CheckIn(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('checked_in', 'Checked In'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="checkin")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    checkin_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"CheckIn - {self.booking.user.username} - {self.status}"


# TicketInstance: stores ticket ID and QR code for each booking
class TicketInstance(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='ticket_instance')
    ticket_id = models.CharField(max_length=100, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.ticket_id} for Booking #{self.booking.id}"
