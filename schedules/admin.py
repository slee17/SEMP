from django.contrib import admin
from .models import Choice, Question

# Register your models here.

#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3 # By default, provide enough fields for 3 choices.

class QuestionAdmin(admin.ModelAdmin):
	# fields = ['pub_date', 'question_text']
	fieldsets = [
		(None,					{'fields': ['question_text']}),
		('Date information', 	{'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [ChoiceInline] # Choice objects are edited on the Question admin page.
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question_text'] # Can add more.

admin.site.register(Question, QuestionAdmin)