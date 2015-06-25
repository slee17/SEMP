from django.apps import AppConfig

class TasksConfig(AppConfig):
	name = 'tasks'
	verbose_name = "Tasks"

	def ready(self):
		import SEMP.userprofile.signals.handlers