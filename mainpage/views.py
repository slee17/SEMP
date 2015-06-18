from django.shortcuts import render

def home(request):
#	context = {'version': 1}
	return render(request, "mainpage/home.html")