import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice
import datetime

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

def create_choice(question_text, choice_text, votes):
    return Choice.objects.create(question_text=question_text, choice_text=choice_text, votes=votes)

def create_question_with_choice(question_text, days, choice_text, votes):
    q = create_question(question_text=question_text, days=days)
    c = create_choice(q, choice_text=choice_text, votes=votes)
    return q,c

class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """
        there is no question to be displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no polls")
        self.assertQuerySetEqual(response.context["questions"], [])

    def test_past_with_choice(self):
        """
        1 question
        - pub_date in the past
        - with choices
        """
        question, _ = create_question_with_choice('question', -1, 'choice', 1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context['questions'], [question])

    def test_past_no_choice(self):
        """
        1 question
        - pub_date in the past
        - without choices
        """
        create_question('', -1)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no polls")
        self.assertQuerySetEqual(response.context["questions"], [])

    def test_2past_with_and_without_choice(self):
        """
        2 questions
        - pub_dates in the past
        - 1 with choices
        - 1 without choices
        """
        question, _ = create_question_with_choice('question', -1, 'choice', 1)
        create_question('', -2)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context['questions'], [question])

    def test_2past_with_choices(self):
        """
        2 questions
        - pub_dates in the past
        - with choices
        """
        question1, _ = create_question_with_choice('question1', -1, 'choice1', 1)
        question2, _ = create_question_with_choice('question2', -2, 'choice2', 2)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context['questions'], [question1, question2])

    def test_2past_without_choices(self):
        """
        2 questions
        - pub_dates in the past
        - without choices
        """
        create_question('question', -1)
        create_question('question', -2)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There is no polls")
        self.assertQuerySetEqual(response.context["questions"], [])

    def test_future_with_choices(self):
        """
        1 question
        - pub_date in the future
        - with choice
        """
        create_question_with_choice('question1', 2, 'choice1', 1)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "There is no polls")
        self.assertQuerySetEqual(response.context["questions"], [])

    def test_future_without_choices(self):
        """
        1 question
        - pub_date in the future
        - without choice
        """
        create_question('question', days=5)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "There is no polls")
        self.assertQuerySetEqual(response.context["questions"], [])

    def test_past_future_with_choices(self):
        """
        2 questions
        - 1 pub_date in the past
        - 1 pub_date in the future
        - with choices
        """
        past_question, _ = create_question_with_choice('question1', -1, 'choice1', 1)
        create_question_with_choice('question2', 1, 'choice2', 1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["questions"], [past_question]
        )


class QuestionDetailViewTest(TestCase):
    def test_past_with_choice(self):
        """
        1 question
        - pub_date in the past
        - with choices
        """
        past_question, _ = create_question_with_choice('question', -1, 'choice', 1)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        response = response.context['object']
        self.assertEqual(response, past_question)

    def test_past_without_choice(self):
        """
        1 question
        - pub_date in the past
        - without choices
        """
        past_question = create_question('question', -1)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_with_choice(self):
        """
        1 question
        - pub_date in the future
        - with choices
        """
        future_question, _ = create_question_with_choice('question', 1, 'choice', 1)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_without_choice(self):
        """
        1 question
        - pub_date in the future
        - without choices
        """
        future_question = create_question('question', 1)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class QuestionResultViewTest(TestCase):
    def test_past_with_choice(self):
        """
        1 question
        - pub_date in the past
        - with choices
        """
        past_question, _ = create_question_with_choice('question', -1, 'choice', 1)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        response = response.context['object']
        self.assertEqual(response, past_question)

    def test_past_without_choice(self):
        """
        1 question
        - pub_date in the past
        - without choices
        """
        past_question = create_question('question', -1)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_with_choice(self):
        """
        1 question
        - pub_date in the future
        - with choices
        """
        future_question, _ = create_question_with_choice('question', 1, 'choice', 1)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_without_choice(self):
        """
        1 question
        - pub_date in the future
        - without choices
        """
        future_question = create_question('question', 1)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
