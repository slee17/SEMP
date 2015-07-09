from django.shortcuts import render

def profile(request):
#	context = {'version': 1}
	return render(request, "accounts/profile.html")