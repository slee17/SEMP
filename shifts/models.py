from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone

from datetime import date, datetime, time, timedelta # For calculating shift duration.
from recurrence.fields import RecurrenceField # For recurring shifts.

class Shift(models.Model):
    """
    Chocies for fields. Edit as necessary.
    """
    DAYS = [
        ('M', 'Monday'),
        ('TU', 'Tuesday'),
        ('W', 'Wednesday'),
        ('TH', 'Thursday'),
        ('F', 'Friday'),
        ('SA', 'Saturday'),
        ('SU', 'Sunday')
    ]
    DEPARTMENTS = (
        ('STAT', 'STAT'),
        ('WC', 'Writing Center'),
        ('ATH', 'Athenaeum')
    )
    LOCATIONS = (
        ('POPPA', 'Poppa'),
        ('SOUTH', 'South'),
        ('RYAL', 'Ryal')
    )
    # RECURRENCE_CHOICES = (
    #    (0, 'None'),
    #    (1, 'Daily'),
    #    (7, 'Weekly')
    # )

    """
    Basic info about the shift.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='shifts',
        blank=True, null=True) # A shift may not have an owner.
    department = models.CharField(max_length=5, choices=DEPARTMENTS, default='STAT')
    location = models.CharField(max_length=25, choices=LOCATIONS, default='Unspecified')
    day_of_the_week = models.CharField(max_length=2, choices=DAYS, blank=True, null=True)
    start_time = models.TimeField(default='12:00:00')
    end_time = models.TimeField(default='14:00:00')
    hours = models.DurationField(editable=False)
    activated = models.BooleanField(verbose_name='Active', default=False)
    spans_past_midnight = models.BooleanField(verbose_name='Spans over midnight', default=False)
    
    """
    Recurrence info about the shift.
    """
    start_date = models.DateField(default=datetime.now) # The start date of the shift (e.g. first day of the semester).
    recurrences = RecurrenceField(default=None)
    # frequency = models.IntegerField(default=0, choices=RECURRENCE_CHOICES)
    # end_date = models.DateField() # The end date of the shift (e.g. last day of the semester).
    # cancelled_date = models.DateField(blank=True, null=True) # Set to a specific date (the date of
                                                             # the cancelled shift) if a shift is cancelled.
    
    """
    Sale info about the shift.
    """
    # on_sale = models.BooleanField(verbose_name='On Sale', default=False)

    """
    For Full Calendar (http://fullcalendar.io/).
    """
    title = models.CharField(max_length=100, blank=True, null=True, editable=False)

    def __unicode__(self):
        return '%s | %s | %s | %s | %s | %s' % (
            unicode(self.department),
            unicode(self.location),
            unicode(self.day_of_the_week),
            unicode(self.start_time),
            unicode(self.end_time),
            unicode(self.owner)
        )

    """
    Methods on an instance of Shift (i.e. row-level).
    """
    def assign_owner(self):
        ACTIVATED_USERS = User.objects.get(activated=True)
        self.owner = models.CharField(choices=ACTIVATED_USERS)

    # def is_on_sale(self):
    #    return self.on_sale

    # def cancel(self, date=None, commit=True):
    #    self.cancelled_date = date or date.today()
    #    if commit:
    #        self.save()

    def save(self, *args, **kwargs): # Overwrite save() to calculate and save the duration of a shift
                                     # and generate a title.

        # As of now, calculating self.hours is a bit hacky because of the way python's datetime work.
        # It works nonetheless.
        adjusted_start_time = datetime.combine(date.today(), self.start_time) # Temporarily use date.today()
                                                                    # to deal with Python's way of calculating datetimes.
                                                                    # http://stackoverflow.com/questions/656297/python-time-timedelta-equivalent 
        adjusted_end_time = datetime.combine(date.today(), self.end_time)
        if self.spans_past_midnight:
            adjusted_end_time += timedelta(days=1) # If the shift spans over midnight, the end date must be a day later.
            if self.start_time < self.end_time: # If the shift starts and ends after midnight:
                adjusted_start_time += timedelta(days=1) # the start date must be a day later as well.
        # Now calculate the duration of the shift through simple subtraction.
        self.hours = adjusted_end_time - adjusted_start_time

        # Set the owner's name as the shift's title, _Unclaimed_ if the shift has no owner.
        """
        if self.owner is None:
            self.title = self.location[0] + "-" + "Unclaimed"
        else:
            self.title = self.location[0] + "-" + str(self.owner)
        """

        super(Shift, self).save(*args, **kwargs)

class Sale(models.Model):
    shift = models.ForeignKey('Shift', related_name='sale') # related_name='sale'
    date = models.DateField(default=datetime.now) # Which date's shift is on sale?
                                                  # Put datetime.now for now and change it to the correct
                                                  # date in views.sales.
    datetime_sold = models.DateTimeField(default=timezone.now)
            # The last datetime the shift was sold.
                # (blank=True, null=True, auto_now_add=True)
                # `auto_now_add=True` allows this field to be automatically set to now when the object is
                # first created. Might need revision.
    datetime_bought = models.DateTimeField(blank=True, null=True) # The last datetime the shift was bought.
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller') # The last seller.
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer', # The last buyer (and thus the current owner).
                                blank=True, null=True) # A sale may not be concluded and there might not be a buyer.