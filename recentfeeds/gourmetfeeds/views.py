from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def welcome(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gourmetfeeds/login/?next=%s' % request.path)
    else:
        return render_to_response('gourmetfeeds/welcome.html',
                                  {},
                                  context_instance=RequestContext(request))
