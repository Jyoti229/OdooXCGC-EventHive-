
from django import forms
from .models import Event, EventFeedback

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'category', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'category': forms.Select(),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = EventFeedback
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your thoughts...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }