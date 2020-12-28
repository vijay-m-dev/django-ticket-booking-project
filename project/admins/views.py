from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from .forms import BusForm
from .models import Bus
from django.contrib import messages
from .filters import BusFilter

# Create your views here.
@login_required()
@allowed_users(allowed_roles=['admins'])
def dashboard(request):
	buses=Bus.objects.all()
	busFilter = BusFilter(request.GET, queryset=buses)
	buses = busFilter.qs 
	context={'buses':buses,'busFilter':busFilter}
	return render(request,'admins/dashboard.html', context)

@login_required()
@allowed_users(allowed_roles=['admins'])
def bus_create(request):
	if request.method == 'POST':
		form=BusForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Bus created')
			return redirect('dashboard')
		else:
			messages.success(request, f'Please fill the form correctly')
			context={'form':form}
			return render(request,'admins/bus_create.html',context)
	form=BusForm()
	context={'form':form}
	return render(request,'admins/bus_create.html',context)

@login_required()
@allowed_users(allowed_roles=['admins'])
def bus_update(request,pk):
	bus=get_object_or_404(Bus,pk=pk)
	if request.method == 'POST':
		form=BusForm(request.POST, instance=bus)
		if form.is_valid():
			form.save()
			messages.success(request, f'Bus Updated')
			return redirect('dashboard')
		else:
			messages.success(request, f'Please fill the form correctly')
			context={'form':form}
			return render(request,'admins/bus_create.html',context)
	form=BusForm(instance=bus)
	context={'form':form}
	return render(request,'admins/bus_create.html',context)

@login_required()
@allowed_users(allowed_roles=['admins'])
def bus_delete(request,pk):
	bus=get_object_or_404(Bus,pk=pk)
	if request.method == 'POST':
		bus.delete()
		messages.success(request, f'Bus Deleted')
		return redirect('dashboard')
	context={'bus':bus}
	return render(request,'admins/bus_delete.html',context)

