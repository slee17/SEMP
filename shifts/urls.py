from django.conf.urls import include, url, patterns
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns(
	'shifts.views',
	url(r'^$', 'home'),
	url(r'^create_sale/$', 'create_sale'),
	url(r'^view_shifts/$', 'view_shifts'),
	url(r'^full_calendar/$', 'full_calendar'),
	# url(r'^fullcalendar/', TemplateView.as_view(template_name="shifts/full_calendar.html"), name='fullcalendar'),
	# url(r'^create_sale/$', views.create_sale, name='create_sale'),
)