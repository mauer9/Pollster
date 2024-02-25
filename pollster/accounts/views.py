from collections import defaultdict
from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView

from .forms import SignupForm, LoginForm, PasswordChangeForm
from pollster.polls.models import Poll, Choice, Vote


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {}
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            # User.objects.create_user() do not take 'confirm_password'
            cleaned_data.pop("confirm_password", None)
            user = User.objects.create_user(**cleaned_data)
            auth_login(request, user)
            return redirect("polls:index")
        else:
            # if there is errors, pass errors to template
            for field in form.fields:
                context[field + "_value"] = request.POST[field]
                context[field + "_css"] = "is-valid"
                if field in form.errors:
                    context[field + "_css"] = "is-invalid"
                    context[field + "_feedback"] = form.errors[field]
    else:
        form = SignupForm()

    context["form"] = form
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("polls:index")

    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("polls:index")
        context["error_message"] = "Sorry, your email and password did not match"
        context["error_css"] = "is-invalid"
    context["form"] = LoginForm()
    return render(request, "accounts/login.html", context)


@login_required(redirect_field_name=None)
def logout(request):
    auth_logout(request)
    return redirect("home")


class VotesView(LoginRequiredMixin, ListView):
    """Show polls that user voted for"""

    redirect_field_name = None
    template_name = "accounts/votes.html"
    context_object_name = "polls"

    def get_queryset(self):
        """queryset of polls that user voted for"""
        if votes := Vote.objects.filter(voter=self.request.user):
            return set(votes)

    def get_context_data(self, **kwargs):
        """
        add 'polls' list to context. 'polls' list contains dict's:
        {
            "text": poll text,
            "id": poll id,
            "count": how many choices user voted for
        }
        """
        context = super().get_context_data(**kwargs)

        # user did not vote for any poll
        if not (all_user_votes := Vote.objects.filter(voter=self.request.user)):
            return context

        polls = defaultdict(int)
        for vote in all_user_votes:
            polls[vote.poll] += 1
        polls = [
            {"text": poll[0].text, "id": poll[0].id, "count": poll[1]}
            for poll in tuple(polls.items())
        ]

        context["polls"] = polls
        return context


class PollsView(LoginRequiredMixin, ListView):
    """Show user created polls"""

    redirect_field_name = None
    template_name = "accounts/polls.html"
    context_object_name = "polls"

    def get_queryset(self):
        return Poll.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def post(self, request, **kwargs):
        pk = request.POST.get("pk")
        poll = get_object_or_404(Poll, pk=pk)

        context = self.get_context_data(**kwargs)
        if poll.author != request.user:
            context["message"] = "You are not author of this poll"
        else:
            poll.delete()

        return self.render_to_response(context)


class EditPollView(LoginRequiredMixin, DetailView):
    """Edit user created poll"""

    redirect_field_name = None
    template_name = "accounts/edit-poll.html"
    context_object_name = "poll"

    def get_queryset(self):
        return Poll.objects.filter(
            created_at__lte=timezone.now(),
            choice__isnull=False,
            author=self.request.user,
        ).distinct()

    def post(self, request, **kwargs):
        poll = self.object = self.get_object()
        poll_choices = poll.choice_set.all()
        new_choices = request.POST.getlist("choices")

        # delete choices
        for poll_choice in poll_choices:
            if poll_choice.text not in new_choices:
                poll_choice.delete()

        # create choices
        poll_choices = [c.text for c in poll_choices]
        for new_choice in new_choices:
            if not new_choice:
                continue
            if new_choice not in poll_choices:
                Choice.objects.create(poll=poll, text=new_choice)

        context = self.get_context_data(**kwargs)
        context["message"] = "Poll updated"
        return self.render_to_response(context)


class PasswordChangeView(LoginRequiredMixin, TemplateView):
    redirect_field_name = None
    template_name = "accounts/change-password.html"

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            context["message"] = "Password successfully updated"
        else:
            # if there is errors, pass errors to template
            for field in form.fields:
                context[field + "_value"] = request.POST[field]
                context[field + "_css"] = "is-valid"
                if field in form.errors:
                    context[field + "_css"] = "is-invalid"
                    context[field + "_feedback"] = form.errors[field]

        return self.render_to_response(context)


class DeleteAccountView(TemplateView):
    template_name = "accounts/delete.html"

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            user = get_object_or_404(User, pk=request.user.pk)
            user.delete()
            context["message"] = "The user is deleted"
        except User.DoesNotExist:
            context["message"] = "User doesnot exist"
        except Exception as e:
            context["message"] = e
        return self.render_to_response(context)
