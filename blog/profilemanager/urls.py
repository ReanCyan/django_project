from django.urls import path
from . import views

app_name = 'profilemanager'
urlpatterns=[
	path('', views.index, name='index'),
	path('login/', views.user_login, name='user_login'),
	path('register/', views.user_register, name='user_register'),
	path('logout/', views.user_logout, name='user_logout')
]