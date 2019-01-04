## Open Issues:
# handle on_delete='CASCADE' issues

from django.conf import settings
from django.urls import reverse
from django.db import models
#from django.utils.text import slugify
from slugify import slugify
from os import path

import re

from django.utils import timezone

import os
import random

import misaka

from groups.models import  Group

from django.contrib.auth import get_user_model
User = get_user_model()

def content_file_name(instance, filename):
    random_int = random.randint(1,99999)
    random_int2 = random.randint(1,99999)
    return os.path.join("QuestionImages", str(instance.user.id), str(random_int2), 
                        str(random_int),filename) 


class Question(models.Model):
#    user = models.ForeignKey(User, related_name="questions",on_delete="CASCADE")
    user = models.ForeignKey(User, related_name="questions")
    created_at = models.DateTimeField(auto_now=True)
    question = models.CharField(unique=False,max_length=500)
    question_html = models.TextField(editable=False,max_length=600)
    question_slug = models.SlugField(allow_unicode=True, unique=False,max_length=600)
#    group = models.ForeignKey(Group, related_name="questions",null=True, blank=True,on_delete="CASCADE")
    group = models.ForeignKey(Group, related_name="questions",null=True, blank=True)
    question_picture = models.FileField(upload_to=content_file_name,null=True,max_length=600) 
    editing_done = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    min_answerers = models.PositiveIntegerField(null=True)
    answerers = models.PositiveIntegerField(default=0)
    due_day = models.TextField(null=True, blank=True)
    due_time = models.TextField(null=True, blank=True)

    
    def __unicode__(self):
        return self.question
    
    def __str__(self):
        return unicode(self).encode('utf-8')
        
    def increase_answerers(self):
        self.answerers += 1
        return self.answerers 
        
    def votesSum(self):
        return sum([answer.votes for answer in self.answers.all()])
        
    # def alreadyVoted(self):
    #     return self.question_answered.filter(user__username__iexact=self.user.username,question=self.question).exists()

    def publish_results(self):
        if self.due_date is None:
            self.due_date = timezone.now()
        if self.min_answerers is None:
            self.min_answerers = 0
        publish_results = (self.due_date < timezone.now()) and (self.answerers >= self.min_answerers )
        return publish_results

    def extension(self):
        name, extension = os.path.splitext(self.question_picture.name)
        return extension[1:]
        
    def save(self, *args, **kwargs):

        self.question = re.sub('<', '&lt ', self.question)
        self.question = re.sub('>', '&gt ', self.question)
        # self.question = re.sub("'", '&#39', self.question)
        # self.question = re.sub('"', '&quot', self.question)
        # self.question = re.sub("&", '&amp', self.question)


        self.question_html = misaka.html(self.question)
        self.question_slug = slugify(self.question)
        super(Question,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "questions:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "question"]
        
class Answer(models.Model):
    created_at = models.DateTimeField(auto_now=True)
#    question = models.ForeignKey(Question, related_name="answers",null=True, blank=True,on_delete="CASCADE")
    question = models.ForeignKey(Question, related_name="answers")
    answer = models.CharField(unique=False,max_length=150)
    votes = models.IntegerField(default='0')


    def __unicode__(self):
        return self.answer
        
    def __str__(self):
        return unicode(self).encode('utf-8')

    def increase_vote(self):
        self.votes += 1
        return self.votes 
        
    def save(self, *args, **kwargs):

        self.answer = re.sub('<', '&lt ', self.answer)
        self.answer = re.sub('>', '&gt ', self.answer)

        super(Answer,self).save(*args, **kwargs)
        

    class Meta:
        ordering = ["created_at"]
        unique_together = ["question","answer"]
        
        
        
class AnswerByUser(models.Model):
    question = models.ForeignKey(Question, related_name="question_answered",null=True)
    answer = models.ForeignKey(Answer, related_name="answered",null=True)
    user = models.ForeignKey(User, related_name="users")
    answered_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group,related_name = "groups",null=True)
    
    def __unicode__(self):
        return "Answer {} by {}".format(self.answer,self.user)
        
    def __str__(self):
        return unicode(self).encode('utf-8')


    class Meta:
        unique_together = ["question","user","group"]

class QuestionVotedByUser(models.Model):
    question = models.ForeignKey(Question, related_name="question_answered_by_user",null=True)
    user = models.ForeignKey(User, related_name="user_voted_question")
    answered_at = models.DateTimeField(auto_now=True)
    answer = models.ForeignKey(Answer, related_name="answered_question_by_user",null=True)
    

    def __unicode__(self):
        return "Question {} by {}".format(self.question.question,self.user.username)
        
    def __str__(self):
        return unicode(self).encode('utf-8')

    class Meta:
        unique_together = ["question","user"]
