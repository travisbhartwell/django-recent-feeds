from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import list_detail

from models import Feed

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
