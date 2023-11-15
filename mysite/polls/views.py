from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):
    questions = Question.objects.order_by("pub_date")
    context = {"questions": questions}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def result(request, question_id):
    return HttpResponse(f"You are looking at results of {question_id}")

def vote(request, question_id):
    return HttpResponse(f"vote for {question_id}")
