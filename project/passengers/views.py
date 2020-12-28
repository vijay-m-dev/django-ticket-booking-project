from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user,allowed_users
from admins.models import Bus
from .models import Booking
from .forms import ProfileForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from admins.filters import BusFilter

# Create your views here.
@login_required()
@allowed_users(allowed_roles=['passengers'])
def home(request):
	buses=Bus.objects.all()
	busFilter = BusFilter(request.GET, queryset=buses)
	buses = busFilter.qs
	bookings=Booking.objects.all().filter(passenger=request.user.passenger)
	context={'buses':buses,'bookings':bookings,'busFilter':busFilter}
	return render(request,'passengers/home.html', context)

@login_required()
@allowed_users(allowed_roles=['passengers'])
def book_ticket(request, pk):
	if request.user.passenger.name is None or request.user.passenger.email is None or request.user.passenger.phone is None:
		messages.success(request, f'Please fill the profile')
		return redirect('home')
	bus = get_object_or_404(Bus,pk=pk)
	if request.method == "POST":
		no_of_tickets=int(request.POST['no_of_tickets'])
		if no_of_tickets>0 and no_of_tickets <= bus.available_seats:
			booking=Booking(passenger=request.user.passenger,bus=bus,no_of_tickets=no_of_tickets)
			booking.save()
			bus.available_seats-=no_of_tickets
			bus.save()
			pk=Booking.objects.filter(passenger=request.user.passenger).last().id
			return redirect('send_email',pk=pk)
		else:
			messages.success(request, f'Not much Tickets available. Available tickets: {bus.available_seats}')
	context={'bus': bus}
	return render(request, 'passengers/book_ticket.html', context)

@login_required()
@allowed_users(allowed_roles=['passengers'])
def delete_ticket(request, pk):
	booking = get_object_or_404(Booking,pk=pk)
	if request.method == "POST":
		booking.delete()
		messages.success(request, f'Booking has been deleted')
		return redirect('home')
	context = {'booking': booking}
	return render(request, 'passengers/delete_ticket.html', context)

@login_required()
def profile(request):
	passenger=request.user.passenger
	if request.method == "POST":
		form=ProfileForm(request.POST, instance=passenger)
		if form.is_valid():
			form.save()
			messages.success(request, f'Profile Updated')
			return redirect('home')		
	form=ProfileForm(instance=passenger)
	context={'form': form}
	return render(request, 'accounts/profile.html', context)

def success(request,pk):
	#pk=Booking.objects.filter(passenger=request.user.passenger).last().id
	passenger=request.user.passenger
	booking=get_object_or_404(Booking,pk=pk)
	bus=booking.bus
	template = render_to_string('passengers/email_template.html',{'booking':booking,'passenger':passenger,'bus':bus})
	email = EmailMessage(
		'Thankyou for Booking tickets',
		template,
		settings.EMAIL_HOST_USER,
		[passenger.email],
		)
	email.fail_silently=False
	email.send()
	messages.success(request, f'Tickets booked and Bill has been sent to {passenger.email}')
	return redirect('home')