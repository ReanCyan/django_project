from django.urls import path
from . import views

app_name = "postmanager"
urlpatterns=[
	path('home/', views.home, name='home'),
	# path('category/'),
	# path('tag/'),
	path('add/', views.add_post, name='add_post'),
	path('<post_slug>/', views.post_detail, name='post_detail')
]