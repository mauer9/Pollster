import datetime
from django.db import models
from django.contrib import admin
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField('date published')

    @admin.display(
        boolean = True,
        ordering='pub_date',
        description='Published recently?'
    )
    def recently_published(self):
        now = timezone.now().date()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @property
    def get_total_votes(self):
        choices = self.choice_set.all()
        total_votes = 0
        for choice in choices:
            total_votes += choice.votes
        return total_votes

    def __str__(self): return self.question_text

class Choice(models.Model):
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self): return self.choice_text
