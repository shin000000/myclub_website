from django.db import models
from django.contrib.auth.models import User

class Venue(models.Model):
	name = models.CharField('Venue name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code', max_length=120)
	phone = models.CharField('Contact Phone', max_length=25, blank=True)
	web =  models.URLField('Website Address', blank=True)
	email_address = models.EmailField('Email Address', blank=True)
	owner = models.IntegerField("Venue Owner", blank=False, default=1)


	def __str__(self):
		return self.name


class MyClubUser(models.Model): 
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField('User Email')


	def __str__(self):
		"""what shows up in the admin area"""
		return self.first_name + ' ' + self.last_name


# Create your models here.
class Event(models.Model):
	name = models.CharField('Event Name', max_length=120)
	event_date = models.DateTimeField('Events Date')
	venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
	manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	description = models.CharField(blank=True, max_length=120)
	attendees = models.ManyToManyField(MyClubUser, blank=True)


	def __str__(self):
		return self.name