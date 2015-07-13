from django.conf.urls import include, url, patterns

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index')
]