## Open Issues:
# Add created_by FK to User
# manage the uniqueness of M2M table also thru created_by
# handle on_delete='CASCADE' issues

from django.conf import settings
from django.urls import reverse
from django.db import models
#from django.utils.text import slugify
from slugify import slugify

import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()



class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User,through="GroupMember")
    created_at = models.DateTimeField(auto_now=True)
#    created_by = models.ForeignKey(User,related_name='user_groups',on_delete="CASCADE")
#    created_by = models.ForeignKey(User,related_name='user_groups')
    
    

    def __str__(self):
        return self.name

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
#        self.created_by = self.request.user.id
        super(Group,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class GroupMember(models.Model):
    # group = models.ForeignKey(Group, related_name="memberships",on_delete="CASCADE")
    # user = models.ForeignKey(User,related_name='user_groups',on_delete="CASCADE")
    # member = models.ForeignKey(User,related_name='GroupMember',on_delete="CASCADE")
    group = models.ForeignKey(Group, related_name="memberships")
    member = models.ForeignKey(User,related_name='user_groups')

    def __str__(self):
        return self.member.username
        
    class Meta:
        unique_together = ("group", "member")