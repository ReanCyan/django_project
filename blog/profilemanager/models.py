from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female'),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
	bio = models.TextField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.user.username

# R&D more on this signal and why it was not working for this case
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Profile.objects.create(user=instance)
# 	else:
# 		instance.profile.save()
