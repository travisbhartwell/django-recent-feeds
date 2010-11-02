from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    user = models.ForeignKey(User)
    source = models.URLField()
    subscribed_date = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=256)

    def __unicode__(self):
        return "[Feed %s for %s]" % (self.title, self.user)


class SeenFeedEntry(models.Model):
    guid = models.CharField(max_length=32)
    user = models.ForeignKey(User)
    first_seen = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "[Entry %s for %s]" % (self.guid, self.user)

