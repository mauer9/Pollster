import random
from django.utils import timezone
from django.contrib.auth.models import User

from polls.models import Poll, Choice, Vote
from faker import Faker

fake = Faker()


def seed_polls(n = 5):
    """
    Create dummy polls

    Args:
        n (int): number of polls to create, 5 by default
    """

    polls = [
        Poll.objects.create(
            author=User.objects.get(pk=1),
            text=fake.sentence()
        )
        for _ in range(n)
    ]
    print("seed polls success")
    return polls


def seed_choices(n = 5, polls = None):
    """
    Create dummy choices for polls

    Args:
        n (int): number of choices to create for each poll, 5 by default
        polls (list): list of polls to create choices for.
            if not specified, create choices for all polls
    """
    if not polls: polls = Poll.objects.all()

    for poll in polls:
        for _ in range(n):
            Choice.objects.create(poll = poll, text = fake.word())
    print("seed choice success")


def seed_votes(n = 30, polls = None):
    """
    Create votes for polls and choices

    Args:
        n (int): number of votes to create for each poll
            30 by default
            randomly distributed among choices
            user is admin
        polls (list): list of polls to create votes for.
            if not specified, create votes for all polls
    """
    if not polls: polls = Poll.objects.all()

    for poll in polls:
        choices = poll.choice_set.all()
        for _ in range(n):
            choice = random.choice(choices)
            Vote.objects.create(voter=User.objects.get(pk=1), poll=poll, choice=choice)
    print("seed votes success")


def seed_all(polls_n = 5, choices_n = 5, votes_n = 30):
    """
    Create polls, choices and votes

    Args:
        polls_n (int): number of polls to create
        choices_n (int): number of choices to create gor each poll
        votes_n (int): number of votes to create for each poll
    """
    polls = seed_polls(polls_n)
    seed_choices(choices_n, polls)
    seed_votes(votes_n, polls)
    print("seed all success")
