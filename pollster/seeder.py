import random
from django.utils import timezone
from django.contrib.auth.models import User

from polls.models import Poll, Choice, Vote
from faker import Faker
fake = Faker()


def seed_polls(n = 5, overwrite = False):
    """
    Create dummy polls

    Args:
        n (int): number of polls to create, 5 by default
        overwrite (bool): overwrite existing polls?
    """
    if overwrite: Poll.objects.all().delete()

    return [
        Poll.objects.create(
            text=fake.sentence(), pub_date=timezone.now()
        )
        for _ in range(n)
    ]

def seed_choices(n = 5, polls = []):
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

def seed_votes(n = 30, polls = []):
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
    admin = User.objects.get(pk=1)

    for poll in polls:
        choices = poll.choice_set.all()
        for _ in range(n):
            choice = random.choice(choices)
            Vote.objects.create(user=admin, poll=poll, choice=choice)

def seed_all(questions_n = 5, choices_n = 2, overwrite = False, new_only = True):
    """
    seed questions and choices
    """
    # new_questions = seed_questions(questions_n, overwrite)
    #
    # if new_only:
    #     seed_choices(choices_n, new_questions)
    # else:
    #     seed_choices(choices_n)

