from django import forms
from .models import Booking, TicketType

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event', 'ticket_type', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        ticket_type = cleaned_data.get('ticket_type')
        quantity = cleaned_data.get('quantity')
        if ticket_type and quantity:
            if hasattr(ticket_type, 'remaining_quantity'):
                if quantity > ticket_type.remaining_quantity:
                    self.add_error('quantity', 'Not enough tickets available.')
        return cleaned_data
