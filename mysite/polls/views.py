from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse # No longer needed since we have HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# Create your views here.

# The Index view
# Initially we used the template loader before 
# implementing the shortcut using render() function
# Now we switched to using Django's Generic Views, which are class based views

# The Index view (class based)
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions
        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")[:5]

# The Detail view (class based)
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

# The Results view (class based)
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# The vote view
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

