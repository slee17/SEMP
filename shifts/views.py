from django.shortcuts import render
# from django.http import HttpResponse

def index(request):
	return render(request, 'shifts/index.html')
	# return HttpResponse('Shift Index')