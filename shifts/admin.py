from django.contrib import admin
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django import forms

from .models import Shift, Sale
from .forms import ShiftAdminForm

class ShiftAdmin(admin.ModelAdmin):
	form = ShiftAdminForm
	list_display = ('department', 'location', 'day_of_the_week', 'start_time', 'end_time',
					'hours', 'owner', 'title', 'activated') # 'start_date', 'end_date', 'get_seller'
	actions = ['activate', 'deactivate', 'assign_owner']

	"""
	def get_seller(self, obj):
		return obj.sale.date
	get_seller.short_description = 'Seller'
	get_seller.admin_order_field = 'sale__seller'
	"""

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

class SaleAdmin(admin.ModelAdmin):
	list_display = ('shift', 'date', 'datetime_sold', 'datetime_bought', 'seller', 'buyer')

admin.site.register(Shift, ShiftAdmin)
admin.site.register(Sale, SaleAdmin) # Make managing sales available on the admin site - sometimes
						  # the admin would want to create and conclude sales (e.g. when the shift-holder
						  # or the buyer has no access to the site).