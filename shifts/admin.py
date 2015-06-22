from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django import forms

from .models import Shift, Sale
from django.contrib.auth.models import User

class ShiftAdmin(admin.ModelAdmin):
	actions = ['activate', 'deactivate', 'assign_owner']

	def activate(self, request, queryset):
		queryset.update(activated=True)
	activate.short_description = "Activate selected shifts"

	def deactivate(self, request, queryset):
		queryset.update(activated=False)
	deactivate.short_description = "Deactivate selected shifts"

	class AssignOwnerForm(forms.Form):
		_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
		owner = forms.ModelChoiceField(User.objects)

	def assign_owner(self, request, queryset):
		form = None

		if 'apply' in request.POST:
			form = self.AssignOwnerForm(request.POST)

			if form.is_valid():
				new_owner = form.cleaned_data['owner']

				queryset.update(owner = str(new_owner))
				
				count = 0
				for shift in queryset:
					count += 1
				plural = ''
				if count != 1:
					plural = 's'

				self.message_user(request, "Successfully assigned %s to %d shift%s." % (new_owner, count, plural))
				return HttpResponseRedirect(request.get_full_path())
		
		if not form:
			form = self.AssignOwnerForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

		return render_to_response('admin/assign_owner.html', {'shifts': queryset, 'owner_form': form},
			context_instance=RequestContext(request))
		assign_owner.short_description = "Assign owner to shifts"

admin.site.register(Shift, ShiftAdmin)