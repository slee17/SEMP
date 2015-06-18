from django.contrib import admin
from .models import Shift, Sale

class ShiftAdmin(admin.ModelAdmin):
	actions = ['activate']

	def activate(self, request, queryset):
#		rows_updated = queryset.update(status='activated')
		queryset.update(status='activated')
	activate.short_description = "Mark selected shifts as activated"

admin.site.register(Shift, ShiftAdmin)