from django.db import models
# from django.contrib.auth.models import User
from registration.supplements import RegistrationSupplementBase

class RegistrationSupplement(RegistrationSupplementBase):
	# user = models.OneToOneField(User, related_name='supplement')
	# first_name = models.CharField("First name", max_length=20)
	# last_name = models.CharField("Last name", max_length=20)
	DEPARTMENTS = (
		('STAT', 'STAT'),
		('WC', 'Writing Center'),
		('ATH', 'Athenaeum'),
	)
	STATUSES = (
		('RGLR', 'Regular'),
		('LEAD', 'Lead'),
		('SPV', 'Supervisor'),
	)
	department = models.CharField("Department", max_length=5, choices=DEPARTMENTS)
	status = models.CharField("Status", max_length=10, choices=STATUSES)

	def __unicode__(self):
		# A summary of this supplement.
		return "%s (%s)" % (self.department, self.status)