from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile', primary_key=True)
		# user is the primary key for the Employee model.
	is_lead = models.BooleanField(default = False)

class Position(models.Model): # Use foreign key to allow a user to have more than one department and/or position.
	user = models.ForeignKey(UserProfile, related_name='positions')
	DEPT = (
		('STAT', 'STAT'),
		('WC', 'Writing Center'),
		('ATH', 'Athenaeum'),
	)

	def get_positions(DEPT):
		POSITIONS = ()
		if DEPT == 'STAT':
			POSITIONS = (('RTA', 'RTA'), ('LTA', 'RTA'), ('MTA', 'RTA'),)
		elif DEPT == 'WC':
			POSITIONS = (('CONS', 'Consultant'))
		elif DEPT == 'Athenaeum':
			POSITIONS = (('SERVER', 'Server'), ('KIT', 'Kitchen'),
				('SECR', 'Security'), ('MD', 'MD'))
		return POSITIONS

	STATUS = (
		('RGLR', 'Regular'),
		('LEAD', 'Lead'),
		('SPV', 'Supervisor'),
	)

	department = models.CharField("Department", max_length=5, choices=DEPT)
	POSITIONS = get_positions(DEPT)
	position = models.CharField("Position", max_length=10, choices=POSITIONS)
	status = models.CharField("Status", max_length=10, choices=STATUS)
