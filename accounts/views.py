from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def signup(request):
	if request.method == 'POST':
		if request.POST['password'] == request.POST['confirm_password']:
			try:
				user = User.objects.get(username=request.POST['username'])
				return render(request, 'accounts/signup.html', {'error': 'Username has already been selected'})
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
				login(request, user)
				return redirect('home')
		else:
			return render(request, 'accounts/signup.html', {'error': 'Passwords did not match. Try again'})
	else:
		return render(request, 'accounts/signup.html')



def loginview(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			if request.POST.get('next') is not None:
				return redirect(request.POST['next'])
			return redirect('home')
		else:
			return render(request, 'accounts/login.html', {'error': 'Username and Password did not match. Try again'})
	else:
		return render(request, 'accounts/login.html')


def logoutview(request):
	if request.method == 'POST':
		logout(request)
		return redirect('home')