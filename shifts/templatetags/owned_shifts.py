from django import template
from shifts.models import Shift

register = template.Library()

@register.inclusion_tag('shifts/owned_shifts.html')
def show_shifts():
	shifts = Shift.objects.all()
	return {'shifts': shifts}