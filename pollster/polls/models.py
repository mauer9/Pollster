from itertools import cycle
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Poll(BaseModel):
    text = models.CharField(max_length=200)

    # import datetime
    # from django.contrib import admin
    # @admin.display(boolean=True, ordering="updated_at", description="Published recently?")
    # def recently_published(self):
    #     now = timezone.now().date()
    #     return now - datetime.timedelta(days=1) <= self.updated_at <= now

    @property
    def total_votes(self):
        return self.vote_set.count()

    def get_choices_with_params(self):
        res = []
        choices = self.choice_set.all()
        choices = choices.annotate(vote_count=models.Count("vote"))
        choices = choices.order_by("-vote_count")
        colors = cycle(
            [
                "info",
                "danger",
                "success",
                "secondary",
            ]
        )

        for choice in choices:
            d = {
                "id": choice.id,
                "text": choice.text,
                "votes": choice.vote_count,
                "color": next(colors),
            }

            d["percent"] = (d["votes"] / self.total_votes) * 100 if d["votes"] else 0

            res.append(d)

        return res

    def __str__(self):
        return self.text


class Choice(BaseModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Vote(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}:{self.choice}:{self.poll}"
