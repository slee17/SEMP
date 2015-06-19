from django.db import models
# from django.contrib.auth.models import User

class Shift(models.Model):
	DAYS = (
		('M', 'Monday'),
		('TU', 'Tuesday'),
		('W', 'Wednesday'),
		('TH', 'Thursday'),
		('F', 'Friday'),
		('SA', 'Saturday'),
		('SU', 'Sunday'),
	)

	DEPARTMENTS = (
		('STAT', 'STAT'),
		('WC', 'Writing Center'),
		('ATH', 'Athenaeum'),
	)
	owner = models.CharField(max_length=25, default='None') # A shift may not have an owner.
	day_of_the_week = models.CharField(max_length=2, choices=DAYS, default='Monday')
	location = models.CharField(max_length=25, default='Unspecified') # Fix later?
	department = models.CharField(max_length=5, choices=DEPARTMENTS, default='STAT')

#	if self.department == 'STAT':
#		CATEGORIES = (
#			('LTA', 'LTA'),
#			('RTA', 'RTA'),
#			('MTA', 'MTA'),
#			('OTA', 'OTA'),
#		)
#	else if self.department == 'WR':
#		CATEGORIES
# 	category = models.CharField(max_length = 25, blank=True)
	
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)

	time = models.TimeField()
#	time = models.DurationField()
	date = models.DateField()
	activated = models.BooleanField(verbose_name = ('Activate'),
									default = False)

	def __unicode__(self):
		return '%s | %s | %s | %s | %s | %s' % (
			unicode(self.department),
			unicode(self.location),
			unicode(self.date),
			unicode(self.day_of_the_week),
			unicode(self.owner),
			unicode(self.activated))
	
	""" 
	Methods on an instance of Shift.
	"""
	def assign_owner(self):
		from django.contrib.auth.models import User
		ACTIVATED_USERS = User.objects.get(activated=True)
		self.owner = models.CharField(max_length, choices=ACTIVATED_USERS)
	# Go with model methods, not managers.
	# def sell(self):
	# def buy(self):

class Sale(Shift): # Multi-table inheritance.
	shift = models.ForeignKey(Shift, related_name='shift_sale')
	seller = models.CharField(max_length=25)
	buyer = models.CharField(max_length=25)
	# date = models.DateField()
	posted = models.DateField(auto_now_add=True)
	bought = models.DateField(auto_now_add=True)
	# was_assigned