from django.contrib import admin
from django.http import HttpResponse
from django.core import serializers

from .models import Shift, Sale

class ShiftAdmin(admin.ModelAdmin):
	actions = ['activate', 'deactivate']

	def activate(self, request, queryset):
		queryset.update(activated=True)
	activate.short_description = "Activate selected shifts"

	def deactivate(self, request, queryset):
		queryset.update(activated=False)
	deactivate.short_description = "Deactivate selected shifts"

#	def assign_owner(self, request, queryset):
#		response = HttpResponse(content_type)
#		queryset.update(owner=)

admin.site.register(Shift, ShiftAdmin)