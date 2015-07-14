from django.contrib import admin
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django import forms

from .models import Shift
from .forms import ShiftAdminForm

class ShiftAdmin(admin.ModelAdmin):
	form = ShiftAdminForm
	list_display = ('department', 'location', 'day_of_the_week', 'start_time', 'end_time', 'hours', 'owner')
	actions = ['activate', 'deactivate', 'assign_owner']

	def activate(self, request, queryset):
		queryset.update(activated=True)
	activate.short_description = "Activate selected shifts"

	def deactivate(self, request, queryset):
		queryset.update(activated=False)
	deactivate.short_description = "Deactivate selected shifts"

	class AssignOwnerForm(forms.Form):
		_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
		owner = forms.ModelChoiceField(get_user_model().objects)

	def assign_owner(self, request, queryset):
		form = None

		if 'apply' in request.POST:
			form = self.AssignOwnerForm(request.POST)

			if form.is_valid():
				new_owner = form.cleaned_data['owner']

				queryset.update(owner = new_owner)
				
				# For plural 's'.
				count = 0
				for shift in queryset:
					count += 1
				plural = ''
				if count != 1:
					plural = 's'

				self.message_user(request, "Successfully assigned %d shift%s to %s." % (count, plural, new_owner))
				return HttpResponseRedirect(request.get_full_path())
		
		if not form:
			form = self.AssignOwnerForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

		return render_to_response('admin/assign_owner.html', {'shifts': queryset, 'owner_form': form},
			context_instance=RequestContext(request))

admin.site.register(Shift, ShiftAdmin)