from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "questions"

    def get_queryset(self):
        queryset = Question.objects
        queryset = queryset.filter(pub_date__lte=timezone.now(), choice__isnull=False)
        queryset = queryset.distinct()
        queryset = queryset.order_by("-pub_date")
        return queryset

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        queryset = Question.objects
        queryset = queryset.filter(pub_date__lte=timezone.now(), choice__isnull=False)
        queryset = queryset.distinct()
        return queryset

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/result.html"

    def get_queryset(self):
        queryset = Question.objects
        queryset = queryset.filter(pub_date__lte=timezone.now(), choice__isnull=False)
        queryset = queryset.distinct()
        return queryset

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You did not select a choice"
            }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:result", args=(question.id,)))
