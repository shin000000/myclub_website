from django.db.models.functions import Lower
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
import csv
from django.contrib import messages

from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# import pagination stuff
from django.core.paginator import Paginator



# generate a pdf file venue list
def event_pdf(request):
	# create bytestream buffer
	buf = io.BytesIO()
	# Create a canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	# Create a text object
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)
	
	# #Add some lines of text
	# lines = [
	# 	'this is line 1',
	# 	'this is line 2',
	# 	'this is line 3',
	# ]

	#designate model
	events = Event.objects.all()

	lines = []

	for event in events:
		lines.append(event.name)
		lines.append(str(event.event_date))
		lines.append(event.venue.name)
		try:
			lines.append(event.manager.username)
		except:
			lines.append("This event has no manager yet.")
		attendees = event.attendees.all()
		attendee_all = ''
		for attendee in attendees:
			attendee_all += attendee.first_name + ' ' + attendee.last_name + '; '
		lines.append(attendee_all)
		lines.append(event.description)
		lines.append("========================================")

	for line in lines:
		textob.textLine(line)

	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	# return something
	return FileResponse(buf, as_attachment=True, filename='events.pdf')


def event_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=events.csv'
	

	# create a csv writer
	writer = csv.writer(response)

	events = Event.objects.all()

	# add column headings to the csv file
	writer.writerow(['Name', 'Event Date', 'Venue', 'Manager', 'Description', 'Attendees'])

	# Loop through venues
	for event in events:
		writer.writerow([event.name, event.event_date, event.venue, event.manager, event.description, event.attendees])

	return response


def event_text(request):
	response = HttpResponse(content_type='text/txt')
	response['Content-Disposition'] = 'attachment; filename=events.txt'

	events = Event.objects.all()

	lines = []

	# Loop through events
	for event in events:
		lines.append(f"{event.name}\n{event.event_date}\n{event.venue}\n{event.manager}\n{event.description}\n{event.attendees}\n\n\n")

	response.writelines(lines)
	return response



# generate a pdf file venue list
def venue_pdf(request):
	# create bytestream buffer
	buf = io.BytesIO()
	# Create a canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	# Create a text object
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)
	
	# #Add some lines of text
	# lines = [
	# 	'this is line 1',
	# 	'this is line 2',
	# 	'this is line 3',
	# ]

	#designate model
	venues = Venue.objects.all()

	lines = []

	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.email_address)
		lines.append("========================================")

	for line in lines:
		textob.textLine(line)

	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	# return something
	return FileResponse(buf, as_attachment=True, filename='venue.pdf')


def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=venues.csv'
	

	# create a csv writer
	writer = csv.writer(response)

	venues = Venue.objects.all()

	# add column headings to the csv file
	writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])

	# Loop through venues
	for venue in venues:
		writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

	return response


def venue_text(request):
	response = HttpResponse(content_type='text/txt')
	response['Content-Disposition'] = 'attachment; filename=venues.txt'

	venues = Venue.objects.all()

	lines = []

	# Loop through venues
	for venue in venues:
		lines.append(f"{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n")

	response.writelines(lines)
	return response


def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('list-venues')


def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user == event.manager:
		event.delete()
		messages.success(request, ('Event deleted!'))
		return redirect('list-events')
	else:
		messages.success(request, ('You are not authrized to delete this event! '))
		return redirect('list-events')

def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None, instance=event)
	else:
		form = EventForm(request.POST or None, instance=event)
	if form.is_valid():
		form.save()
		return redirect('list-events')

	return render(request, 'events/update_event.html', 
		{'event': event, 'form': form})


def add_event(request):
	submitted = False
	if request.method == "POST":
		# if request.user.id == ...
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/add_event?submitted=True')
		else:
			form = EventForm(request.POST)
			if form.is_valid():
				event = form.save(commit=False)
				event.manager = request.user #logged in user id
				event.save()
				return HttpResponseRedirect('/add_event?submitted=True')
		
	else:
		if request.user.is_superuser:
			form = EventFormAdmin
		else:
			form = EventForm
		if 'submitted' in request.GET:
			submitted = True 
	return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance=venue)
	if form.is_valid():
		form.save()
		return redirect('list-venues')

	return render(request, 'events/update_venue.html', 
		{'venue': venue, 'form': form})


def search_venues(request):
	if request.method == "POST":
		searched = request.POST['searched']
		venues = Venue.objects.filter(name__contains=searched)
		return render(request, 'events/search_venues.html', 
			{'searched': searched, 'venues': venues})
	else:
		return render(request, 'events/search_venues.html', {})


def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue_owner = User.objects.get(pk=venue.owner)
	return render(request, 'events/show_venue.html', 
		{'venue': venue,
		 'venue_owner': venue_owner,
		 })


def list_venues(request):
	# venue_list = Venue.objects.all()

	# set up pagination
	order = 'name'
	if 'order' in request.GET:
		order = request.GET.get('order')
	venue_list = Venue.objects.all().order_by(order)
	p = Paginator(venue_list, 5)
	page = request.GET.get('page')
	venues = p.get_page(page)
	nums = "a" * venues.paginator.num_pages

	return render(request, 'events/venues.html', 
		{'venues': venues, 'nums': nums})


def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			venue = form.save(commit=False)
			venue.owner = request.user.id #logged in user id
			venue.save()
			# form.save()
			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True 
	return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def all_events(request):
	order = 'name'
	if 'order' in request.GET:
		order = request.GET.get('order')
	date_now = datetime.now
	event_list = Event.objects.all().order_by(Lower(order))
	return render(request, 'events/event_list.html', 
		{'event_list': event_list, 
		'order': order,
		'date_now': date_now
		})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = 'cynthia'
	month = month.capitalize()
	# convert month from name to number 
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	# create a Calendar
	cal = HTMLCalendar().formatmonth(year, month_number)
	# get current year
	now = datetime.now()
	current_year = now.year

	# get current time
	time = now.strftime('%I:%M:%S %p')

	return render(request, 'events/home.html', {
		'name': name,
		'year': year,
		'month': month,
		"month_number":month_number,
		"cal": cal,
		"current_year": current_year,
		"time": time,
		})


