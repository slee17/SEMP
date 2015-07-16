from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse

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
    activated = models.BooleanField(verbose_name='Activate', default=False)
    sale_status = models.BooleanField(verbose_name='Activate sale', default=False)
    
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
        self.owner = models.CharField(choices=ACTIVATED_USERS)

    def activate_sale(self):
        self.sale_status = True

    def deactivate_sale(self):
        self.sale_status = False

    def save(self, *args, **kwargs): # Overwrite save() to calculate and save the duration of a shift.
        temp_date = datetime(1,1,1,0,0,0)
        self.hours = datetime.combine(temp_date, self.end_time) - datetime.combine(temp_date, self.start_time)
        super(Shift, self).save(*args, **kwargs)

    def day_url(year, month, day, has_shift, *args, **kwargs):
        """
        Returns a link to the page for the given day or None if there is not to be a day link.
        has_shift is a boolean telling this method whether there is a shift on the day or not.
        """
        return HttpResponse("Hello world.")

    def month_url(year, month, *args, **kwargs):
        """
        Returns a link to the page for the given month or None if there is not to be a month link.
        """
        return HttpResponse("Hello world.")

    def shifts_by_day(year, month, *args, **kwargs):
        """
        Returns a dictionary mapping the day number to a list of shifts on that day.
        """
        return {1: [Shift.objects.get(pk=1)]}

    #    def sell(self, *args, **kwargs):
    #        seller = self.owner

class Sale(models.Model):
    shift = models.ForeignKey(
        Shift,
        limit_choices_to={'sale_status': True}, # Only create Sale if sale_status has been set to True.
        related_name='shift_sale'
    )
    on_sale = models.BooleanField(verbose_name=('On sale'), default=False)
    # ACTIVATED_USERS = User.objects.get(activated=True)
    # seller = models.CharField(choices=ACTIVATED_USERS)
    # buyer = models.CharField(choices=ACTIVATED_USERS)
    sold = models.DateField(blank=True, null=True)