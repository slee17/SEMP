from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import JsonResponse

from .models import Shift
from .forms import ShiftSaleForm

import json

# CONTROLS_LOCKED = False

def index(request):
	return render(request, 'shifts/index.html')
"""
def shift_sale(request):
	if request.method == 'POST':
		shift_sale = request.POST.get('')
"""