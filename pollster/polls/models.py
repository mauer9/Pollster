import datetime
import random
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
        total_votes = [choice.votes for choice in self.choice_set.all()]
        total_votes = sum(total_votes)
        return total_votes

    def get_choices_with_params(self):
        res = []
        choices = self.choice_set.all().order_by('-votes')

        colors = ['warning', 'danger', 'success', 'primary',]
        while len(colors) < choices.count(): colors.extend(colors)
            
        for choice in choices:
            d = {}
            d['id'] = choice.id
            d['text'] = choice.choice_text
            d['votes'] = choice.votes

            d['color'] = colors.pop()

            d['percent'] = 0
            if d['votes'] != 0:
                d['percent'] = (d['votes'] / self.get_total_votes) * 100

            res.append(d)

        return res

    def __str__(self): return self.question_text

class Choice(models.Model):
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self): return self.choice_text
