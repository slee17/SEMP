import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
# Models: essentialy database layout (with additional metadata)
class Question(models.Model): # Each model is represented by a class that subclasses django.db.models.Model
							  # Each model has a number of class variables.
	question_text = models.CharField(max_length=200) # Each class variable represents a database field in the model.
													 # Each field is represented by an instace of a Field class (e.g. CharField, DateTimeField).
													 # Field's name = column name: question_text
	pub_date = models.DateTimeField('date published')
	
	def __unicode__(self): # To return a helpful representation of the object.
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
	question = models.ForeignKey(Question) # Relationship defined.
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	def __unicode__(self):
		return self.choice_text