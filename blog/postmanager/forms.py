from django import forms
from .models import Post

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('category', 'title', 'content', 'tags', 'post_slug', 'public_visible',)