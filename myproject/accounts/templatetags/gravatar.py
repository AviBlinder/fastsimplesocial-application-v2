import urllib, hashlib


from django import template
from django.conf import settings

register = template.Library()


#https://fi.gravatar.com/site/implement/images/python/

@register.filter
def gravatar(user):
    email = user.email.lower().encode('utf-8')
    default = 'mm'
    size = 256
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    
    return gravatar_url
    
