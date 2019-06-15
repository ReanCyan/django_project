from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def start(request):
	return redirect('blog:user_login')

def user_login(request):
	return HttpResponse("Hello, World!",)

def user_register(request):
	if request.method == "POST":
		form = ProfileForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Registration Successful!!")
			login(request, user)
			messages.info(request, f"You are logged in as '{username}'")
			return redirect('blog:home')
		else:
			for msg in form.error_messages:
				messages.error(request,f"Oops! Wrong Input. Check for Errors")
				#messages.error(request,f"{form.error_messages[msg]}")	
				return render(request=request, template_name="blog/register.html",context={"form": form})
	form = ProfileForm
	return render(request = request,
			template_name = 'blog/register.html',
			context = {'form': form})