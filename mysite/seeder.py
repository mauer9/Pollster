from django.utils import timezone
from polls.models import Question, Choice
from faker import Faker
fake = Faker()


def seed_questions(n = 5):
    """
    create dummy questions, 5 by default
    """
    for _ in range(n):
        q = Question.objects.create(question_text = fake.sentence(), pub_date=timezone.now())

def seed_choices(n = 2):
    """
    create choices for each question, 2 choice per question by default
    """
    questions = Question.objects.all()
    for question in questions:
        for _ in range(n):
            Choice.objects.create(question_text = question, choice_text = fake.word())
