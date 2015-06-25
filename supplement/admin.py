from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import RegistrationSupplement
"""
# Define an inline admin descriptor for MyRegistrationSupplement models
# which acts a bit like a singleton
class RegistrationSupplementInline(admin.StackedInline):
	model = RegistrationSupplement
	can_delete = False
	verbose_name_plural = 'supplement information'

# Define a new User admin
class UserAdmin(UserAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'supplement_department', 'is_active', 'is_staff')
	def supplement_department(self, x):
		return x.supplement.department
	inlines = (RegistrationSupplementInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
"""