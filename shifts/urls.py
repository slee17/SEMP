from django.conf.urls import include, url, patterns

from . import views

urlpatterns = patterns(
	'shifts.views',
	url(r'^$', 'home'),
	url(r'^create_sale/$', 'create_sale')
	# url(r'^create_sale/$', views.create_sale, name='create_sale'),
)