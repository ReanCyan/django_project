from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.

class TutorialCategory(models.Model):
	tutorial_category = models.CharField(max_length=100)
	category_summary = models.CharField(max_length=100)
	category_slug = models.CharField(max_length=100)

	class Meta:
		# Gives the proper plural name for admin
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.tutorial_category

class TutorialSeries(models.Model):
	tutorial_series = models.CharField(max_length=100)

	tutorial_category = models.ForeignKey(TutorialCategory, default=1, verbose_name="Categories", on_delete=models.SET_DEFAULT)
	series_summary = models.CharField(max_length=100)

	class Meta:
		# otherwise we get "Tutorial Seriess in admin"
		verbose_name_plural = "Series"

	def __str__(self):
		return self.tutorial_series

class Tutorial(models.Model):
	tutorial_title = models.CharField(max_length=100)
	tutorial_content = models.TextField()
	tutorial_published = models.DateTimeField('date published')
	tutorial_series = models.ForeignKey(TutorialSeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
	tutorial_slug = models.CharField(max_length=100, default=1)

	def __str__(self):
		return self.tutorial_title

class Question(models.Model):
	question_text = models.CharField(max_length=100)
	pub_date = models.DateTimeField('ques_date_published', default=datetime.now())

	def __str__(self):
		return self.question_text
	
	def was_published_recently(self):
		return timezone.now() - timedelta(days=1) <= self.pub_date <= timezone.now()

	was_published_recently.admin_order_field = "pub_date"
	was_published_recently.boolean = True
	was_published_recently.short_description = "Published  Recently?"

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length = 50)
	votes = models.IntegerField(default = 0)