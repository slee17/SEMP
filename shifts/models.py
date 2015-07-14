from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from datetime import date, datetime, time, timedelta # For calculating shift duration.

class Shift(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='shifts',
        blank=True, null=True) # A shift may not have an owner.

    # Choices for fields. Add more choices as necessary.
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
    LOCATIONS = (
        ('POPPA', 'Poppa'),
        ('SOUTH', 'South'),
        ('RYAL', 'Ryal'),
        ('ATH', 'Ath'),
    )

    day_of_the_week = models.CharField(max_length=2, choices=DAYS, blank=True, null=True)
    location = models.CharField(max_length=25, choices=LOCATIONS, default='Unspecified') # TODO
    department = models.CharField(max_length=5, choices=DEPARTMENTS, default='STAT')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(default='12:00:00')
    end_time = models.TimeField(default='14:00:00')
    hours = models.DurationField(editable=False) # DurationField is an interval in PostgreSQL.
    activated = models.BooleanField(verbose_name=('Activate'), default=False)
    on_sale = models.BooleanField(verbose_name=('On sale'), default=False) # editable=False?

    def __unicode__(self):
        return '%s | %s | %s | %s | %s | %s' % (
            unicode(self.department),
            unicode(self.location),
            unicode(self.day_of_the_week),
            unicode(self.start_time),
            unicode(self.end_time),
            unicode(self.owner)
        )
    
    # Methods on an instance of Shift (i.e. row-level).
    def assign_owner(self):
        ACTIVATED_USERS = User.objects.get(activated=True)
        self.owner = models.CharField(max_length, choices=ACTIVATED_USERS)

    def save(self, *args, **kwargs): # Overwrite save() to calculate and save the duration of a shift.
        temp_date = datetime(1,1,1,0,0,0)
        self.hours = datetime.combine(temp_date, self.end_time) - datetime.combine(temp_date, self.start_time)
        super(Shift, self).save(*args, **kwargs)

#    def sell(self, *args, **kwargs):
#        seller = self.owner


    # Go with model methods, not managers.
    # def sell(self):
    # def buy(self):

# class Sale(Shift): # Multi-table inheritance.
# shift = models.ForeignKey(Shift, related_name='shift_sale')