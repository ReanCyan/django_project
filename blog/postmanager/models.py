from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
	category_name = models.CharField(max_length=32)
	category_slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
	
	class Meta:
		verbose_name_plural = 'Catergories'

	def __str__(self):
		return self.category_name

	def _get_unique_slug(self):
		category_slug = slugify(self.category_name)
		unique_slug = category_slug
		num = 1
		while Category.objects.filter(category_slug=unique_slug).exists():
			unique_slug = f'{category_slug}-{num}'
			num+=1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.category_slug:
			self.category_slug = self._get_unique_slug()
		super().save(*args, **kwargs)

class Tag(models.Model):
	tag_name = models.CharField(max_length=32)
	tag_slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)

	class Meta:
		verbose_name_plural = 'Tags'

	def __str__(self):
		return self.tag_name

	def _get_unique_slug(self):
		tag_slug = slugify(self.tag_name)
		unique_slug = tag_slug
		num = 1
		while Tag.objects.filter(tag_slug=unique_slug).exists():
			unique_slug = f'{tag_slug}-{num}'
			num+=1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.tag_slug:
			self.tag_slug = self._get_unique_slug()
		super().save(*args, **kwargs)

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, related_name= 'posts', on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag)
	title = models.CharField(max_length=100)
	content = models.TextField(default="")
	created_on = models.DateTimeField(default=timezone.now)
	updated_on = models.DateTimeField(default=timezone.now)
	post_slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
	public_visible = models.BooleanField(default=True)

	class Meta:
		verbose_name_plural = 'Posts'

	def __str__(self):
		return self.title

	def _get_unique_slug(self):
		post_slug = slugify(self.title)
		unique_slug = post_slug
		num = 1
		while Post.objects.filter(post_slug=unique_slug).exists():
			unique_slug = f'{post_slug}-{num}'
			num+=1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.post_slug:
			self.post_slug = self._get_unique_slug()
		super().save(*args, **kwargs)

# R&D how to manage likes and comments on this posts.

class PostImages(models.Model):
	post = models.ForeignKey(Post, related_name= 'images', on_delete = models.CASCADE)
	# 'related_name' attribute specifies the name of the reverse relation from post model back to this model. Ex, Post.images.all()
	# If you don't specify a related_name, Django automatically creates one using the name of your model with the suffix _set, for instance Post.postimages_set.all().
	post_image = models.ImageField(upload_to='post_images/%Y/%m/%d', null=True, blank=True)

	class Meta:
		verbose_name_plural = 'PostImages'

	def __str__(self):
		return self.post.title + "Image"