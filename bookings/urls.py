# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.event_list, name="event_list"),
    path("events/<int:event_id>/book/", views.booking_form, name="booking_form"),
    path("payment/<int:booking_id>/confirm/", views.payment_confirm, name="payment_confirm"),
    path("checkin/scan/", views.checkin_scan, name="checkin_scan"),
    path("organizer/dashboard/", views.organizer_dashboard, name="organizer_dashboard"),
]
