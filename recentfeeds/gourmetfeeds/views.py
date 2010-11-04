from functools import reduce
import logging
import operator

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail

from models import Feed, SeenFeedEntry
import delicious

logger = logging.getLogger(__name__)

def welcome(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('login/?next=%s' % request.path)
    else:
        return render_to_response('gourmetfeeds/welcome.html',
                                  {},
                                  context_instance=RequestContext(request))


@login_required
def feeds(request):
    queryset = Feed.objects.filter(user=request.user).order_by('subscribed_date')

    return list_detail.object_list(request, queryset)


def rss(request, username, path):
    user = get_object_or_404(User, username=username)

    source_url = delicious.get_source_url_from_path(path)
    our_url = delicious.get_url(source_url, username)

    # Just retrieve to make sure the feed is subscribed to
    get_object_or_404(Feed, user=user, source=source_url)

    rssFeed = delicious.DeliciousFeedRss(source_url, our_url)

    guids = rssFeed.get_item_guids()

    query_list = [Q(guid__exact=guid) for guid in guids]
    guid_query = reduce(operator.or_, query_list)

    already_seen = SeenFeedEntry.objects.filter(Q(user=user),
                                                guid_query)
    for item in already_seen:
        rssFeed.remove_item_with_guid(item.guid)

    guids_left = rssFeed.get_item_guids()
    for item in guids_left:
        entry = SeenFeedEntry(guid=item, user=user)
        entry.save()

    response = HttpResponse(rssFeed.get_rss())
    response['Content-Type'] = 'application/rss+xml; charset=utf-8'
    return response

