from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
	formfield_overrides ={
		models.TextField : {'widget' : TinyMCE()}
	}

admin.site.register(Profile, ProfileAdmin)
