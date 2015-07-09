from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

"""
User - Position (foreign key: one-to-many)
"""

class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', primary_key=True)
		# user is the primary key for the Employee model.
	
class Position(models.Model): # Use foreign key to allow a user to have more than one department and/or position.
	# user = models.ForeignKey(UserProfile, related_name='positions')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='positions')
	DEPT = (
		('STAT', 'STAT'),
		('WC', 'Writing Center'),
		('ATH', 'Athenaeum'),
	)
	
	POSITIONS = (
		('LTA', 'LTA'),
		('RTA', 'RTA'),
		('MTA', 'MTA'),
		('CONS', 'Consultant'),
		('SERVER', 'Server'),
		('KIT', 'Kitchen'),
		('SECR', 'Security'),
		('MD', 'MD'),
	)

	STATUS = (
		('RGLR', 'Regular'),
		('LEAD', 'Lead'),
		('SPV', 'Supervisor'),
	)

	department = models.CharField("Department", max_length=5, choices=DEPT)
	position = models.CharField("Position", max_length=10, choices=POSITIONS)
	status = models.CharField("Status", max_length=10, choices=STATUS)

	def __unicode__(self):
		return '%s | %s' % (self.department, self.status)