from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import Category, Tag, Post, PostImages

# Register your models here.
class PostImagesInline(admin.TabularInline):
	model = PostImages
	extra = 3

class PostAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.TextField: {'widget': TinyMCE()},
	}
	inlines = [PostImagesInline]

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)