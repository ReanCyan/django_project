from django.urls import path
from . import views

app_name = 'main' # namespacing of urls
urlpatterns = [
	# ex: /main/
	path('', views.IndexView.as_view(), name='index'),

	#ex: /main/2/
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	
	#ex: /main/2/results/
	path('<int:pk>/results/', views.ResultsView.as_view(), name="results"),

	#ex: /main/2/vote/
	path('<int:question_id>/vote/', views.vote, name="vote"),

	#ex: /main/display/
	path('display/', views.tutorial_display, name='display'),

	#ex: /main/display/python/
	path('display/<single_slug>/', views.single_slug, name='single_slug'),

	#ex: /main/register/
	path('register/', views.register, name="register"),

	#ex: /main/login/
	path('login/', views.login_request, name="login"),

	#ex: /main/logout/
	path('logout/', views.logout_request, name="logout"),

	#ex: /main/community
	path('community/', views.community, name="community"),

	#ex: /main/next_question
	path('<int:question_id>/next_question/', views.next_question, name="next_question")
]
