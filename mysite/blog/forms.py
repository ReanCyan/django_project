from django import forms
from .models import Profile
from django.core.files.images import get_image_dimensions

class UserCreateForm(forms.ModelForm):
	#email = forms.EmailField(required=True)
	class Meta:
		model = Profile

	def clean_avatar(self):
		avatar = self.cleaned_data['avatar']

		try:
			w, h = get_image_dimensions(avatar)

			# validate dimenstions
			max_width = max_hight = 100
			if w >max_width or h>max_hight:
				raise forms.ValidationError(f"Please use image that is {max_width}x{max_hight} or smaller.")

			# validate content type
			main, sub = avatar.content_type.split('/')
			if not(main == 'image' and sub in ['jpeg', 'png', 'gif', 'pjpng']):
				raise forms.ValidationError("Please use a JPEG, PNG pr GIF image")

			# validate file size
			if len(avatar) > (20*1024):
				raise form.ValidationError("Avatar file size may not exceed 20k")

		except AttributeError:
			# Hendles cases when we are updating the user Profile
			# and do not supply a new avatar
			pass