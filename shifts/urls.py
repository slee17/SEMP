from django.conf.urls import include, url, patterns

from . import views

urlpatterns = patterns(
	'shifts.views',
	url(r'^$', views.index, name='index'),
	url(r'^create_sale/$', 'create_sale'),
)