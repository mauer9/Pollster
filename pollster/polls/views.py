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
def vote(request, id):
    redirect = HttpResponseRedirect(reverse("polls:detail", args=(id,)))

    if request.method != "POST":
        return redirect

    poll = get_object_or_404(Poll, id=id)
    user = request.user
    choice = poll.choice_set.filter(id=request.POST["choice"]).first()
    # poll without choices
    if not choice:
        return render(
            request,
            "polls/detail.html",
            {"question": poll, "error_message": "You did not select a choice"},
        )

    # admin can vote unlimited time
    if user.is_superuser:
        Vote.objects.create(user=user, poll=poll, choice=choice)

        return redirect

    # if among all votes
    if all_votes := Vote.objects.filter(user=user):
        # user voted for current poll
        if poll_vote := all_votes.filter(poll=poll).first():
            # then update the vote
            poll_vote.choice = choice
            poll_vote.save()

            return redirect

    # user do not have any votes or did not vote for current poll
    Vote.objects.create(user=user, poll=poll, choice=choice)

    return redirect
