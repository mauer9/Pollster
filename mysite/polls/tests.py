from django.test import TestCase
<<<<<<< Updated upstream

# Create your tests here.
=======
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTest(TestCase):
    def test_recently_published_with_future_question(self):
        """
        Question.recently_published() returns False for
        posts published in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.recently_published(), False)

    def test_recently_published_with_old_question(self):
        """
        Question.recently_published() returns False for
        posts pub_date older than a day
        """
        time = timezone.now() - datetime.timedelta(hours=24)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.recently_published(), False)

    def test_recently_published_with_recent_question(self):
        """
        Question.recently_published() returns True for
        posts with pub_date within last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.recently_published(), True)


def create_question(question_text, days):
    """
    Create a question with question_text as question_text,
    negative days means create question in the -X days past
    positive days means create question in the +X days future
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """
        if there is no question - test for appropriate message
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no polls")
        self.assertQuerySetEqual(response.context["questions"], [])

    def test_past_questions(self):
        """
        question(s) from the past are displayed in the index page
        """
        question = create_question('past question', days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["questions"], [question]
        )

    def test_future_questions(self):
        """
        question(s) with pub_date in the future are
        not displayed in the index page
        """
        create_question('future question', days=5)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "There is no polls")
        self.assertQuerySetEqual(response.context["questions"], [])

    def test_past_and_future_questions(self):
        """
        question(s) with pub_date in the future are
        not displayed in the index page
        but from past are
        """
        question = create_question('past question', days=-5)
        create_question('future question', days=5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["questions"], [question]
        )

    def test_two_past_questions(self):
        """
        all question(s) from the past are displayed in the index page
        """
        question1 = create_question('past question1', days=-5)
        question2 = create_question('past question2', days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["questions"], [question1, question2]
        )
>>>>>>> Stashed changes
