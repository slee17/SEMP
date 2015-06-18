from django.db import models
from registration.supplements import RegistrationSupplementBase

class MyRegistrationSupplement(RegistrationSupplementBase):
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
	status = models.CharField("Status", max_length=5, choices=STATUSES)

	def __unicode__(self):
		# A summary of this supplement.
		return "%s (%s)" % (self.department, self.status)