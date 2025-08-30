from django.contrib import admin
from .models import Booking, Payment, CheckIn, TicketInstance


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "ticket_type", "quantity", "total_price", "payment_status", "booking_date")
    list_filter = ("payment_status", "event")
    search_fields = ("user__username", "event__title")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "method", "status", "transaction_id", "amount", "timestamp")
    list_filter = ("status", "method")
    search_fields = ("transaction_id", "booking__user__username")


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "status", "checkin_time")
    list_filter = ("status",)
    search_fields = ("booking__user__username", "booking__event__title")


@admin.register(TicketInstance)
class TicketInstanceAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "ticket_id", "created_at")
    search_fields = ("ticket_id", "booking__user__username")
