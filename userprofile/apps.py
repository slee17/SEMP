"""
The following code was to ensure that a UserProfile is created whenever a User is created.
from django.apps import AppConfig

class TasksConfig(AppConfig):
	name = 'tasks'
	verbose_name = "Tasks"

	def ready(self):
		import SEMP.userprofile.signals.handlers
"""