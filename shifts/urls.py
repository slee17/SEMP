from django.conf.urls import include, url, patterns
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns(
	'shifts.views',
	url(r'^$', 'home'),
	url(r'^view_shifts/$', 'view_shifts', name='view_shifts'),
	url(r'^full_calendar/$', 'full_calendar'),
	url(r'^view_shifts/sales/$', 'sales', name='sales'),
	# url(r'^view_shifts/buy/$', 'buy', name='buy'),
	# url(r'^fullcalendar/', TemplateView.as_view(template_name="shifts/full_calendar.html"), name='fullcalendar'),
	# url(r'^create_sale/$', views.create_sale, name='create_sale'),
)