from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    user = models.ForeignKey(User)
    source = models.URLField()

    def __unicode__(self):
        return "[Feed %s for %s]" % (self.source, self.user)

class SeenFeedEntry(models.Model):
    guid = models.CharField(max_length=32)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "[Entry %s for %s]" % (self.guid, self.user)

