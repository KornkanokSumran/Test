from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

def homepage (request):
    return render(request,'polls/homepage.html')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def delete_question(request):
    q = request.POST.get['question']
    qname = ''
    try:
        qname += '\'' + Question.objects.get(pk=q.id).question_text + '\''
    except (KeyError, Question.DoesNotExist):
        return render(request, 'polls/Question.html', { 'error_message': "You didn't select a question.",
        })
    else:
        qname = str(len(q)) + "Question"
        question = Question.objects.get(pk=q.id)
        question.delete()

    # for i in q:
    #     if(len(qname)<50):
    #         qname += '\'' + Question.objects.get(pk=i).question_text + '\''
    #     else:
    #         qname = str(len(q)) + "Question"
    #     question = Question.objects.get(pk=i)
    #     question.delete()
    return render(request, 'polls/Question.html',{'latest_question_list': question.objects.all(),'question_de': qname + 'Deleted'})

def remove(request):
    return render(request, 'polls/Question.html')