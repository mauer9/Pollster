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
        queryset = Poll.objects.filter(
            pub_date__lte=timezone.now(), choice__isnull=False
        )
        queryset = queryset.distinct()
        return queryset.order_by("-pub_date")


class DetailView(generic.DetailView):
    model = Poll
    template_name = "polls/detail.html"

    def get_queryset(self):
        queryset = Poll.objects.filter(
            pub_date__lte=timezone.now(), choice__isnull=False
        )
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.get_object()
        choices = poll.get_choices_with_params()
        context["choices"] = choices

        if not self.request.user.is_authenticated:
            return context

        # if user already voted in the current pole
        # pass the choice to template so voted choice will be checked
        all_user_votes = Vote.objects.filter(user=self.request.user)
        vote = all_user_votes.filter(poll=poll).first()
        if vote:
            context["user_choice"] = vote.choice

        return context


@login_required(redirect_field_name=None)
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
