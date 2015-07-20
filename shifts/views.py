from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse

from .models import Shift
from .forms import ShiftSaleForm

import json

# CONTROLS_LOCKED = False

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
    return HttpResponse('shifts/full_calendar.html')
#    tmpl_vars
#    return render(request, 'shifts/full_calendar.html', tmpl_vars)

def view_shifts(request):
    activated_shifts = Shift.objects.filter(activated=True)
    shifts = []
    for shift in activated_shifts:
        shifts.append({'id': shift.id, 'department': shift.department, 'start_date': shift.start_date})
    # return HttpResponse(json.dumps(shifts, cls=DjangoJSONEncoder), mimetype='application/json')
    # return JsonResponse(shifts, safe=False)
    return render(request, 'shifts/full_calendar.html',
        {'shifts': json.dumps(shifts)})

def create_sale(request):
    if request.method == 'POST':
    	shift_sale_status = request.POST.get('the_shift')
    	response_data = {}

    	# Grab the shift id along with its new sale status and update the database.
    	shift = Shift.objects.get(pk=1)
    	shift.sale_status = not shift.sale_status
    	shift.save()

    	# Create a response dict, serialize it into JSON, and send it as the response.
    	response_data['result'] = 'Successfully created shift sale.'
    	response_data['shiftpk'] = shift.pk
    	response_data['sale_status'] = shift.sale_status
    	response_data['sold'] = shift.sold.strftime('%B %d, %Y %I:%M %p')
    	response_data['seller'] = shift.owner.username

    	return JsonResponse(response_data)

    else:
    	return JsonResponse({"Nothing to see": "this isn't happening."})