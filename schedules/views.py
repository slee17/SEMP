from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect #HttpResponse
#from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

#def index(request):
#	latest_question_list = Question.objects.order_by('-pub_date')[:5]
##	template = loader.get_template('polls/index.html') # Load the template.
##	context = RequestContext(request, { # Pass a context to the template.
										# Context is a dictionary mapping template variable names to Python objects.
##		'latest_question_list': latest_question_list,
##	})
##	return HttpResponse(template.render(context))
#	context = {'latest_question_list': latest_question_list}
#	return render(request, 'polls/index.html', context) # Render handles loading a template, filling a context, and returning an HttpResponse.
														# render() takes the request object, a template name, (a dictionary).
														# render() returns an HttpResponse object of the given template rendered with the given context.

#def detail(request, question_id):
##	try:
##		question = Question.objects.get(pk=question_id)
##	except Question.DoesNotExist:
##		raise Http404("Question does not exist")
#	question = get_object_or_404(Question, pk=question_id) # get_object_or_404() takes a Django model and an arbitrary number of keyword arguments.
														   # There's also get_list_or_404().
#	return render(request, 'polls/detail.html', {'question': question})
	## return HttpResponse("You're looking at question %s." % question_id)

#def results(request, question_id):
#	question = get_object_or_404(Question, pk=question_id)
#	return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView): # ListView: display a list of objects.
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list' # The automatically generated context variable for ListView is question_list.
												 # To override, we provide the context_object_name attribute.

	def get_queryset(self):
	    """
	    Return the last five published questions (not including those set to be
	    published in the future).
	    """
	    return Question.objects.filter(
	        pub_date__lte=timezone.now() # returns a queryset containing Questions whose pub_date is <= timezone.now.
	    ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView): # DetailView: display a detail page for a particular type of object.
									  # For DetailView, the question variable is provided automatically.
									  # (The templates are provided with a context that contains the question and latest_question_list context variables.)
									  # Since we're using a Django model (Question), Django is able to determine an appropriate name for the context variable.
	model = Question # Each generic view needs to know what model it will be acting upon.
	template_name = 'polls/detail.html' # By default, DetailView uses a template <app name>/<model name>_detail.html. Here, it would use polls/question_detail.html.
										# template_name tells Django to use a specific template name instead of the autogenerated default template name.
	def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html' # We also specify template_name to ensure that the results view and the detail view have a different appearance when rendered,
										 # even though they are both a DetailView behind the scenes.

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice']) # request.POST is a dictionary-like object that lets you access submitted data by key name.
        															  # request.POST['choice'] returns the ID of the selected choice, as a string.
        															  # request.POST values are always strings.
        															  # request.GET also accesses GET data in the same way.
        															  # But using request.POST ensures that data is only altered via a POST call.
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,))) # HttpResponseRedirect takes the URL to which the user will be redirected.
        																	# this reverse() will return a string '/polls/3/results'