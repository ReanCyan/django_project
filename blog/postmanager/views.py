from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from profilemanager.models import Profile
from .models import Post, PostImages
from .forms import PostForm
from django.forms import modelformset_factory
from django.views import generic
from django.urls import reverse
from django.contrib import messages

def home(request):
	public_posts = Post.objects.filter(public_visible=True)
	thumbnail_images = {}
	for post in public_posts:
		first_image = PostImages.objects.filter(post_id = post.id).first()
		thumbnail_images[post] = first_image.post_image
	return render(request, 'postmanager/home.html', context={'public_posts': public_posts, 'thumbnail_images': thumbnail_images})

# class HomeView(generic.ListView):
# 	template_name = 'postmanager/home.html'
# 	context_object_name = 'latest_posts'

# 	def get_query(self):
# 		return  Post.objects.all()

def add_post(request):
	PostImagesFormSet = modelformset_factory(PostImages, fields=('post_image',), extra=3)
	if request.method == "POST":
		form = PostForm(request.POST)
		formset = PostImagesFormSet(request.POST or None, request.FILES or None)
		if form.is_valid() and formset.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			# You must add ManyToMany Relation after both models have the value required to create that realtion 
			# so we need to save form before we can add or connect tags to post.
			for tags in request.POST.getlist('tags'):
				post.tags.add(tags)
			for f in formset:
				try:
					postimages = PostImages(post=post, post_image=f.cleaned_data['post_image'])
					postimages.save()
				except Exception as e:
					continue
			return HttpResponseRedirect(reverse('postmanager:home'))
		else:
			messages.error(request, "Oops!! Something Went Wrong")
			return render(request=request, template_name='postmanager/add_post.html', context={'form':form, 'formset': formset})
	
	form = PostForm()
	formset = PostImagesFormSet(queryset=PostImages.objects.none())
	return render(request=request, template_name='postmanager/add_post.html', context = {'form': form, 'formset': formset})

def post_detail(request, post_slug):
	post = Post.objects.get(post_slug = post_slug)
	post_images = PostImages.objects.filter(post_id = post.id)
	return render(request=request, template_name = 'postmanager/post_detail.html', context = {'post': post, 'post_images': post_images})