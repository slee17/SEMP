from django.conf.urls import url
from . import views

urlpatterns = [ # Using generic views.
	# ex: /polls/
	url(r'^$', views.IndexView.as_view(), name='index'),
	
	# ex: /polls/5/
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'), # When not using generic views, we used <question_id> instead of <pk>.
																		  # DetailView expects the primary key value captured from the  URL to be called "pk".
	
	# ex: /polls/5/results
	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'), # When not using generic views, we used <question_id> instead of <pk>.
	
	# ex: /polls/5/vote/
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]