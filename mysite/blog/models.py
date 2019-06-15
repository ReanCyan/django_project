from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', blank=True)

	class Meta:
		app_label = 'blog'

	def __str__(self):
		return self.user.username