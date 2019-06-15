from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from .models import Tutorial, Question, Choice, TutorialCategory, TutorialSeries
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from .forms import NewUserForm
from django.utils import timezone

#from django.http import HttpResponse -- method to use for HTTP Responeses
#from django.template import loader -- method to use for rendering template without render() function

# Create your views here.
class IndexView(generic.ListView):#request, *args, **kwargs):
	template_name = 'main/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('id')[:5]		
	#latest_question_list = Question.objects.order_by('id')[:5]
	#context = {
	#	'latest_question_list' : latest_question_list,	
	#}
	#return render(request, 'main/index.html', context)

class DetailView(generic.DetailView):#request, question_id):	
	#question = get_object_or_404(Question, id = question_id)
	#return render(request,'main/detail.html',{'question':question})
	model = Question
	template_name = 'main/detail.html'
	
	def get_queryset(self):
		"""
		Excludes any question that aren't published yet
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):#request, question_id):
	model = Question
	template_name = 'main/results.html'	
	#question = get_object_or_404(Question, pk = question_id)
	#return render(request, 'main/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'main/detail.html', {'question': question, 'error_message': "You Didn't Vote"})
	else:
		selected_choice.votes += 1;
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
        	# with POST data. This prevents data from being posted twice if a
        	# user hits the Back button.
		return HttpResponseRedirect(reverse('main:results', args=(question.id,)))

def community(request):
	# That creates a flat list of all ids.
	#questions = Question.objects.values_list('id', flat=True)
	# If you want more than one field per row, you can't do a flat list. This will create a list of tuples:
	# questions = Question.objects.value_list('id','question_text')
	#question = 1;
	#if request.method == "POST" and question_id > question:
	#	question_id += 1
	#	return HttpResponseRedirect(reverse('main:detail', args=(question_id,)))
	#else:
	#	return HttpResponseRedirect(reverse('main:detail', args=(question,)))
	question = 1
	return HttpResponseRedirect(reverse('main:detail', args=(question,)))

def next_question(request, question_id):
	if request.method == "POST":
		questions = Question.objects.values_list('id', flat=True)
		# for qus in questions:
		# 	if question_id == qus:
		#question_id +=1
		# Check for last one
		if question_id in questions:
			nxt_qus = Question.objects.filter(id__gt = question_id).order_by('id').first()
			return HttpResponseRedirect(reverse('main:detail', args=(nxt_qus.id,)))
		else:
			messages.info(request, "Nice Job! You made it to the otherside!")
			return redirect("main:display")

def tutorial_display(request):
	return render(request,
	      template_name="main/categories.html",
	      context={"categories": TutorialCategory.objects.all})

def single_slug(request, single_slug):
	categories = [c.category_slug for c in TutorialCategory.objects.all()]
	if single_slug in categories:
		matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
		series_urls={}
		for m in matching_series.all():
			part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest('tutorial_published')
			series_urls[m] = part_one.tutorial_slug
		return render(request, 'main/category.html', context={'tutorial_series':matching_series, 'part_ones': series_urls})

	tutorials = {t.tutorial_slug for t in Tutorial.objects.all()}
	if single_slug in tutorials:
		this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)
		tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by('tutorial_published')
		this_tutorial_index = list(tutorials_from_series).index(this_tutorial)
		return render(request, 'main/tutorial.html', context = {'tutorial':this_tutorial, 'sidebar':tutorials_from_series, 'this_t_idx':this_tutorial_index})
	
	return HttpResponse(f"{single_slug} doesn't correspond to anything we know of!")

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Registration Successful!!")
			login(request, user)
			messages.info(request, f"You are logged in as '{username}'")
			return redirect('main:display')
		else:
			for msg in form.error_messages:
				messages.error(request,f"Oops! Wrong Input. Check for Errors")
				#messages.error(request,f"{form.error_messages[msg]}")	
				return render(request=request, template_name="main/register.html",context={"form": form})
	form = NewUserForm
	return render(request = request,
			template_name = 'main/register.html',
			context = {'form': form})

def logout_request(request):
	logout(request)
	messages.success(request, "Logged out successfully!")
	return redirect("main:display")

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are logged in as '{username}'")
				return redirect("main:display")
			else:
				messages.error(request, "Invalid Username or Password")
		else:
			messages.error(request, "Invalid Username or Password")

	form = AuthenticationForm()
	return render(request = request,
		      template_name = "main/login.html",
		      context = {'form': form})
