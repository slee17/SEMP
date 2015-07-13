from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Shift

# CONTROLS_LOCKED = False

def index(request):
	return render(request, 'shifts/index.html')