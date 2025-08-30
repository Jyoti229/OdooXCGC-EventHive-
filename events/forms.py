from django import forms
from .models import EventFeedback

class CommentForm(forms.ModelForm):
    class Meta:
        model = EventFeedback
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your thoughts...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
