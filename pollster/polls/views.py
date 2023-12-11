from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Poll, Choice, Vote


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "polls"

    def get_queryset(self):
        queryset = Poll.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False)
        queryset = queryset.distinct()
        queryset = queryset.order_by("-pub_date")
        return queryset

class DetailView(generic.DetailView):
    model = Poll
    template_name = "polls/detail.html"

    def get_queryset(self):
        queryset = Poll.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False)
        queryset = queryset.distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.get_object()
        choices = poll.get_choices_with_params()
        context['choices'] = choices
        return context

@login_required
def vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    user = request.user
    try:
        choice = poll.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": poll,
                "error_message": "You did not select a choice"
            }
        )
    else:
        Vote.objects.create(user=user, poll=poll, choice=choice)
        return HttpResponseRedirect(reverse("polls:detail", args=(poll.id,)))
