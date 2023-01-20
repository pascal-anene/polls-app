from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
from django.template import loader 

from .models import Question

# Create your views here.

# The Index view
# Initially we used the template loader before 
# implementing the shortcut using render() function
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list,} 
    return render(request, "polls/index.html", context)

# The Detail view
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist") # possible squiggly line showing nonexistence in pylance
    return render(request, "polls/detail.html", {"question": question})

# The Results view
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

# The vote view
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


