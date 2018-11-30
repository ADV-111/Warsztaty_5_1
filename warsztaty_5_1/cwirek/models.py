from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    content = models.CharField()
    creation_date = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
