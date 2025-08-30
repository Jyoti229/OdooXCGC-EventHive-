from django.contrib import admin
from .models import Booking, Payment, CheckIn

admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(CheckIn)

# Register your models here.
