from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm
from accounts.decorators import unauthenticated_user, login_redirect
from django.contrib import messages



@unauthenticated_user
def registerPage(request):
	form=UserForm()
	if request.method == 'POST':
		form=UserForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Account created')
			return redirect('login')
	context={'form': form }
	return render(request,'accounts/register.html', context)



@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username_or_email=request.POST.get('username_or_email')
		password=request.POST.get('password')
		user = authenticate(request, username=username_or_email, password=password)
		if user is not None:
			login(request, user)
			return login_redirect(request)
		user = authenticate(request, email=username_or_email, password=password)
		if user is not None:
			login(request, user)
			return login_redirect(request)
	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	messages.success(request, f'Logged out')
	return redirect('login')

