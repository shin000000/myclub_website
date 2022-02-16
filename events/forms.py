from django import forms 
from django.forms import ModelForm
from .models import Venue, Event


# Create a venue form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		# fields = "__all__"
		fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address')
		labels = {
			'name': '',
			'address': '',
			'zip_code': '',
			'phone': '',
			'web': '',
			'email_address': ''
		}
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
			'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
			'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zip_code'}),
			'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
			'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'web'}),
			'email_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email_address'})
		}

# admin superuser event form
class EventFormAdmin(ModelForm):
	class Meta:
		model = Event
		# fields = "__all__"
		fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description', )
		labels = {
			'name': '',
			'event_date': 'YYYY-MM-DD HH:MM:SS',
			'venue': 'Venue',
			'manager': 'Manager',
			'attendees': 'Attendees',
			'description': '',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
			'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'event_date'}),
			'venue': forms.Select(attrs={'class': 'form-control', 'placeholder': 'venue'}),
			'manager': forms.Select(attrs={'class': 'form-control', 'placeholder': 'manager'}),
			'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendees'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}),
		}

class EventForm(ModelForm):
	class Meta:
		model = Event
		# fields = "__all__"
		fields = ('name', 'event_date', 'venue', 'attendees', 'description', )
		labels = {
			'name': '',
			'event_date': 'YYYY-MM-DD HH:MM:SS',
			'venue': 'Venue',
			'attendees': 'Attendees',
			'description': '',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
			'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'event_date'}),
			'venue': forms.Select(attrs={'class': 'form-control', 'placeholder': 'venue'}),
			'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendees'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}),
		}