"""SEMP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url # Note: django.conf.urls.defaults has been removed since Django 1.6.
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Regular expressions for the include() functions don't have a $ but rather a trailing slash.
	# When Django encounters include(), it chops off whatever part of the URL matched up to that point
	# and sends the remaining string to the included URLconf for further processing.
    url(r'^$', include('mainpage.urls')), # mainpage.views.home
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/', include('registration.backends.default.urls')), # Not sure where this is from but Python complains about the use of urls.
    url(r'^registration/', include('registration.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^shifts/', include('shifts.urls')),
]