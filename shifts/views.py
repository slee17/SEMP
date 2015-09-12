#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from .models import Shift, Sale
# from .forms import ShiftSaleForm

from collections import OrderedDict # _events_ in _calendar_config_options_
from datetime import date, datetime, timedelta

import json

def home(request):
    try:
        shifts = Shift.objects.get(pk=1)
    except Shift.DoesNotExist:
        shifts = None
    tmpl_vars = {
        'all_shifts': Shift.objects.reverse(),
        'shifts': shifts
    }
    return render(request, 'shifts/index.html', tmpl_vars)

def full_calendar(request):
    return render(request, 'shifts/fullcalendar_index.html')

def view_shifts(request):
    """Render the calendar template with all activated shifts."""
    activated_shifts = Shift.objects.filter(activated=True) # Get all the activated shifts.
    shifts = [] # place holder
    start_time = '8:00:00' # default starting time
    end_time = '22:00:00' # default end time

    if not activated_shifts: # If there are no activated shifts,
        return render(request, 'shifts/calendar_init.html') # return an empty calendar.

    for shift in activated_shifts:
        # Set the start time according to the earliest shift.
        temp_start_time = str(shift.start_time)
        if temp_start_time < start_time:
            start_time = temp_start_time
            if temp_start_time == '00:00:00': # Account for shifts that span over midnight.
                start_time = '08:00:00'
        # Set the end time according to the latest shift.
        temp_end_time = str(shift.end_time)
        if shift.spans_past_midnight == True: # Account for shifts that span over midnight.
            temp_end_time = str(datetime.combine(date.today(), shift.end_time) + timedelta(hours=24))
        if temp_end_time > end_time:
            end_time = temp_end_time

    header = {'left': 'prev,next today',
              'center': 'title',
              'right': 'month,agendaWeek,agendaDay'}
    editable = 'false'
    show_all_day = 'false'
    all_day_default = 'false' # Events are all-day by default. Change that behavior to false. This will
                              # render events in agendaWeek and agendaDay views, 
    weekends = 'true'
    view = 'agendaWeek'
    first_day = '1'
    start_time = "8:00:00"
    end_time = "26:00:00"

    event_sources = []

    # Appending all shifts at the locations. Brute forcing for now to account for different styles
    # for shifts at different labs but will ultimately be changed.
    event_sources.append({'events': get_shifts('POPPA'), 'color': '#981A31', 'textColor': 'white'})
    event_sources.append({'events': get_shifts('SOUTH'), 'color': '#9E7C0A', 'textColor': 'white'})
    event_sources.append({'events': get_shifts('RYAL'), 'color': '#00546B', 'textColor': 'white'})

    # Temp
    shift = get_object_or_404(Shift, pk=100)

    return render(request, 'shifts/calendar_init.html',
        {'header': header,
         'editable': editable,
         'show_all_day': show_all_day,
         'all_day_default': all_day_default,
         'show_weekends': weekends,
         'default_view': view,
         'first_day': first_day,
         'start_time': start_time,
         'end_time': end_time,
         'event_sources': event_sources,
         'event_render': event_render(),
         # 'events': json.dumps(shifts)
         'shift': shift
         })

def get_shifts(location):
    """Return the active shifts at location in JSON format."""
    # Get all the activated shifts at the location.
    activated_shifts = Shift.objects.filter(activated=True, location=location)
    shifts = [] # place holder

    for shift in activated_shifts: # shift represents a recurrence, as opposed to an instance.
        # Get all the occurrence dates of the shift starting from the first day of the shift.
        dates = shift.recurrences.occurrences(
                dtstart=datetime.combine(shift.start_date, shift.start_time))
        
        for date in dates:
            start_time = shift.start_time
            end_time = shift.end_time

            # Check whether or not the shift time needs adjustment.
            if shift.spans_past_midnight:
                # If it does (i.e. shift spans over midnight), let's first adjust the end hour.
                temp_hour = shift.end_time.hour
                adjusted_hour = temp_hour + 23
                end_time = str(adjusted_hour) + ":" + "59:00"
                    # Really hacky, but Full Calendar does not render events as expected if the added
                    # hour goes over 24. `temp = datetime.combine(date.date(), shift.end_time) + timedelta(days=1)`
                    # is essentially what these calculations are trying to do.

                # Now let's look at the start time. Check if the start time is after midnight by
                # comparing it to the end time. Note that, if a shift spans past midnight, the end time
                # must be after midnight (and thus likely a small number, e.g. 2:00:00). This means
                # that if the start time is smaller than the end time (e.g. 1:00:00 < 2:00:00) then
                # the start time is after midnight as well. In such a case, adjust the start time.
                if shift.start_time < shift.end_time:
                    temp_hour = shift.start_time.hour
                    adjusted_hour = temp_hour + 23
                    start_time = str(adjusted_hour) + ":59:00"
            
            # Format the start and end datetimes to fit FullCalendar's requirements.
            start = str(date.date()) + 'T' + str(start_time)
            end = str(date.date()) + 'T' + str(end_time)

            sale_status = False
            # Check if the shift is on the date is on sale.
            if is_on_sale(shift.id, date):
                sale_status = True

            # A custom field for brief description of a shift instance. It includes the minimum
            # essential information about the shift.
            description = str(shift.day_of_the_week) + "<br>" + \
                          str(shift.start_time) + "-" + str(shift.end_time) + "<br>" \
                          "Owner: %s" % str(shift.owner)

            # Append the minimum required information about the shift to the place holder.
            shifts.append({'id': shift.id, 'title': str(shift.title), 'start': start, 'end': end,
                           'description': description, 'sale_status': str(sale_status)}) # 'sale_status': sale_status
    return shifts
    
def get_latest_sale(shift_id, shift_date):
    """ A helper function that gets the latest sale of a shift instance.
    input: the ID of the shift, the date of the shift instance
    output: the latest sale object associated with the shift """
    # Get the shift.
    shift = get_object_or_404(Shift, pk=shift_id)
    # Get the latest sale for shift instance. Note that this returns a QuerySet.
    sale = Sale.objects.filter(shift=shift, date=shift_date)
    # If there is something in the QuerySet...
    if sale.exists():
        return sale.latest('datetime_sold')
    # Return None if the shift has never been sold.
    return None

def get_current_owner(shift_id, shift_date):
    shift = Shift.objects.get(pk=shift_id)
    latest_sale = get_latest_sale(shift_id, shift_date)    
    # If the shift has never been on sale before...
    if latest_sale == None:
        # Then the original owner is also the current owner.
        current_owner = shift.owner
    # Otherwise (i.e. if the shift has been on sale before)...
    else: 
        on_sale = is_on_sale(shift_id, shift_date)
        if on_sale:
            current_owner = latest_sale.seller
        else:
            current_owner = latest_sale.buyer
    return current_owner

def is_on_sale(shift_id, shift_date):
    """ Returns true if the shift instance is on sale; false otherwise.
    """
    latest_sale = get_latest_sale(shift_id, shift_date)
    # If the shift has never been sold then it's not currently on sale either.
    if latest_sale == None:
        return False
    # If the latest sale of the shift does not have a buyer, then the shift is still on sale.
    if latest_sale.buyer == None:
        return True
    else:
        return False

def event_render():
    render_function = """function(event, element) {
                        $(element).find(".fc-time").remove();
                    }"""
    return render_function

@login_required # If the user isn’t logged in, redirect to settings.LOGIN_URL, passing the current
                # absolute path in the query string. (e.g. /accounts/login/?next=/polls/3/)
                # If the user is logged in, execute the view normally. The view code is free to
                # assume the user is logged in.
                # For more info: https://docs.djangoproject.com/en/1.8/topics/auth/default/#django.contrib.auth.decorators.login_required
def sales(request):
    shift_id = request.POST.get('shift_id')
    unprocessed_shift_datetime = request.POST.get('date') # "Fri Sep 11 2015 12:00:00 GMT+0000"
    shift_date = datetime.strptime(unprocessed_shift_datetime[:-9], "%a %b %d %Y %H:%M:%S")
        # Ignore the timezone part and format rest of the string into datetime.
    shift = get_object_or_404(Shift, pk=shift_id)
    owner = get_current_owner(shift_id, shift_date)
    if 'sell' in request.POST:
        # Is the requester authorized to sell the shift? (i.e. requester is the current owner of the shift)
        if request.user == owner:
            # If so, create a sale with fields filled with appropriate values.
            sale = Sale.objects.create(shift=shift, seller=request.user, date=shift_date) # datetime_sold=datetime.now
                # sale = Sale.objects.create is equivalent to sale = Sale(), sale.save(force_insert=True).
                # request.POST is a dictionary-like object that lets you access submitted data by key name.
                    # In this case, request.POST['date'] returns the date of the selected shift, as a string.
                    # request.POST values are always strings.
        else:
            raise PermissionDenied
    elif 'buy' in request.POST:
        sale = get_latest_sale(shift_id, shift_date)
        sale.buyer = request.user
        sale.save()
    return HttpResponseRedirect(reverse('shifts:view_shifts'))