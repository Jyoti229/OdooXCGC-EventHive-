# forms.py for CustomUser registration and login
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
	ROLE_CHOICES = [
		('organizer', 'Organizer'),
		('attendee', 'Attendee'),
	]
	name = forms.CharField(max_length=150, required=True)
	email = forms.EmailField(required=True)
	role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
	phone = forms.CharField(max_length=20, required=False)

	class Meta:
		model = CustomUser
		fields = ['name', 'email', 'role', 'phone', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
	username = forms.EmailField(label='Email', max_length=254)
