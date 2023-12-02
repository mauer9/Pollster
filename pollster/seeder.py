from django.utils import timezone
from polls.models import Question, Choice
from random import randint
from faker import Faker
fake = Faker()


def seed_questions(n = 5, overwrite = False):
    """
    create dummy questions
    """
    if overwrite: Question.objects.all().delete()

    return [
        Question.objects.create(
            question_text=fake.sentence(), pub_date=timezone.now()
        )
        for _ in range(n)
    ]

def seed_choices(n = 2, questions = []):
    """
    create choices for questions
    if questions not specified, create choices for all questions
    """
    if not questions: questions = Question.objects.all()

    for question in questions:
        for _ in range(n):
            Choice.objects.create(
                choice_text = fake.word(),
                question_text = question,
                votes = randint(0, 10)
            )

def seed_all(questions_n = 5, choices_n = 2, overwrite = False, new_only = True):
    """
    seed questions and choices
    """
    new_questions = seed_questions(questions_n, overwrite)

    if new_only:
        seed_choices(choices_n, new_questions)
    else:
        seed_choices(choices_n)

