from django.contrib import admin
from .models import Tutorial, TutorialSeries, TutorialCategory, Question, Choice
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
	fieldsets = [
		  ("Title/Date",{'fields': ["tutorial_title", "tutorial_published"]}),
		  ("URL",{'fields':["tutorial_slug"]}),
		  ("Series",{'fields':["tutorial_series"]}),
		  ("Content",{'fields': ["tutorial_content"]})
	]
	formfield_overrides = {
		models.TextField: {'widget': TinyMCE()}	
	}

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields':["question_text"]}),
		('Date information',{'fields':["pub_date"]}),
	]
	inlines = [ChoiceInline]
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	list_filter = ["pub_date"]
	search_fields = ["question_text"]

#class ChoiceAdmin(admin.ModelAdmin):
#	fields = ["choice_text",
#		  "question",
#		  "votes"]

admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice, ChoiceAdmin)
