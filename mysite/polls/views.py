from django.http import Http404
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F

from django.views.generic.list import ListView

from .models import Question, Choice


class IndexView(ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"


def show_all_questions(request):
    all_questions_list = Question.objects.order_by("-pub_date")
    context = {
        "all_questions_list": all_questions_list,
    }
    return render(request, "polls/all-questions.html", context)


def about(request):
    return render(request, "polls/about.html")


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_list = question.choice_set.all()
    return render(request, "polls/detail.html", {"question": question, "choices": choice_list})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_list = question.choice_set.all()
    try:
        selected_choice = choice_list.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "choices": choice_list,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
