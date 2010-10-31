from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    user = models.ForeignKey(User)
    source = models.URLField()

class SeenFeedEntry(models.Model):
    guid = models.CharField(max_length=32)
    user = models.ForeignKey(User)


