#!/usr/bin/python3.7
from django import template
from ..models import Comments

register = template.Library()


@register.filter()
def count_comments(tweet):
    comments = Comments.objects.filter(tweet_id=tweet.id)
    return len(comments)
