from django.db import models
from django.contrib.auth.models import User

# UserProfile for extra info
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


# Event Categories
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# Event Model
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Ticket Types for each event
class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_types")
    name = models.CharField(max_length=100)   # General, VIP, Student, Early Bird
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_start = models.DateTimeField(null=True, blank=True)
    sale_end = models.DateTimeField(null=True, blank=True)
    max_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"



    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


# Favorite Events
class FavoriteEvent(models.Model):
    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


# Optional: Promo Codes / Discounts
class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    event = models.ForeignKey(Event, related_name="promotions", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"


class EventFeedback(models.Model):
    event = models.ForeignKey('Event', related_name='feedbacks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  # ye add karo
    rating = models.IntegerField(default=5)  # ye add karo
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

