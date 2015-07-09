from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import UserProfile, Position

from shifts.models import Shift

"""
# Define an inline admin descriptor for the Position model
class PositionInline(NestedStackedInline):
	model = Position
	can_delete = False

# Define an inline admin descriptor for the UserProfile model
class UserProfileInline(NestedStackedInline):
	model = UserProfile
	can_delete = False
	inlines = [PositionInline]
"""

class PositionsInline(admin.StackedInline):
	model = Position
	can_delete = False

class ShiftsInline(admin.StackedInline):
	model = Shift
	can_delete = False

# Define a new User admin
class UserAdmin(UserAdmin):
# class UserAdmin(NestedModelAdmin):
	# model = User
	# list_display = ['username', 'get_department']
	"""
	def get_is_lead(self, obj):
		return '%s' % (obj.profile.is_lead)
	get_is_lead.short_description = 'is_lead'
	"""
	def get_department(self, obj):
		return ",".join([k.department for k in obj.profile.positions_set.all()])
		# return '%s' % (obj.profile.positions.department)

	get_department.short_description = 'department'
	# inlines = (PositionsInline, )
	inlines = (PositionsInline, ShiftsInline, )
	# inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(get_user_model())
admin.site.register(User, UserAdmin)
