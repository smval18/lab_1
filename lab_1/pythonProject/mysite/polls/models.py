import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class NewUser(AbstractUser):
    photo_avatar = models.ImageField(max_length=254, verbose_name='Avatar', upload_to='media/avatarka', blank=False)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    description = models.TextField(max_length=4000)
    brief_description = models.TextField(max_length=300)
    question_vote = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    photo = models.ImageField(max_length=254, upload_to='media/question', blank=True)

    @property
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def get_percent(self):
        percent = self.votes * 100 / self.question.question_vote
        return percent


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.question_text
