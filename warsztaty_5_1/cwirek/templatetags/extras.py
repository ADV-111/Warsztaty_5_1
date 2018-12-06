#!/usr/bin/python3.7
from django import template
from ..models import Comments

register = template.Library()


@register.filter()
def count_comments(tweet):
    comments = Comments.objects.filter(tweet_id=tweet.id)
    return len(comments)


@register.filter()
def first_signs(message):
    short_message = str(message)[0:30]
    if len(message) > 30:
        short_message += '...'
    return short_message
