from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Feed(models.Model):
    user = models.ForeignKey(User)
    source = models.URLField(verify_exists=True)
    subscribed_date = models.DateTimeField(auto_now_add=True,
                                           default=datetime.now)
    title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=256, default='')

    class Meta:
        unique_together = [('user', 'source')]

    def __unicode__(self):
        return "[Feed %s for %s]" % (self.title, self.user)


class SeenFeedEntry(models.Model):
    guid = models.CharField(max_length=32)
    user = models.ForeignKey(User)
    first_seen = models.DateTimeField(auto_now_add=True,
                                      default=datetime.now)

    class Meta(object):
        unique_together = [('guid', 'user')]

    def __unicode__(self):
        return "[Entry %s for %s]" % (self.guid, self.user)

