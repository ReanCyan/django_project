from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
	path('', views.start, name="start"),
	path('login/', views.user_login, name="user_login"),
	#path('', views.profile, name="profile")
	path('register/', views.user_register, name="user_register"),
]