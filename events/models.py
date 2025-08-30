from django.db import models
class Event(models.Model):
    CATEGORY_CHOICES = (
        ('workshop', 'Workshop'),
        ('concert', 'Concert'),
        ('sports', 'Sports'),
        ('hackathon', 'Hackathon'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_types")
    name = models.CharField(max_length=100)   # General, VIP, etc.
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_start = models.DateTimeField(null=True, blank=True)
    sale_end = models.DateTimeField(null=True, blank=True)
    max_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"