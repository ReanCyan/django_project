from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm, ProfileForm
from django.urls import reverse
from django.contrib import messages

def index(request):
	return redirect('profilemanager:user_login')

def user_login(request):
	if request.method == "POST":
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are logged in as '{username}'")
				return HttpResponseRedirect(reverse('postmanager:home'))
			else:
				messages.error(request, "Invalid Username or Password")
		else:
			messages.error(request, "Invalid Username or Password")
	
	form = AuthenticationForm()
	return render(request = request, 
				template_name= 'profilemanager/login.html',
				context= {'form':form})

def user_logout(request):
	logout(request)
	messages.success(request, "Logged out successfully!")
	return redirect("profilemanager:index")

def user_register(request):
	if request.method == "POST":
		user_form = UserCreateForm(request.POST)
		profile_form = ProfileForm(request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.save()
			profile = profile_form.save(commit = False)
			profile.user = user
			if 'avatar' in request.FILES:
			 	profile.avatar = request.FILES['avatar']
			else:
				gender = profile_form.cleaned_data.get('gender')
				if gender == 'M':
					profile.avatar = 'none/default_male.png'
				else:
					profile.avatar = 'none/default_female.png'
			profile.save()
			username = user_form.cleaned_data.get('username')
			messages.success(request, f"Registration Successful!!")
			login(request, user)
			messages.info(request, f"You are logged in as '{username}'")
			return HttpResponseRedirect(reverse('postmanager:home'))
		else:
			messages.error(request,"Oops! Wrong Input. Check for Errors")
			# for msg in user_form.error_messages:
				# messages.error(request,f"{user_form.error_messages[msg]}")
			return render(request=request, template_name="profilemanager/register.html",context={"user_form": user_form, "profile_form": profile_form})
	else:
		user_form = UserCreateForm()
		profile_form = ProfileForm()
		return render(request = request,
				template_name = 'profilemanager/register.html',
				context = {'user_form': user_form, 'profile_form': profile_form})