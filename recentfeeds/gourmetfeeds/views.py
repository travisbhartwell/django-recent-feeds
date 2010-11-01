from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def welcome(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gourmetfeeds/login/?next=%s' % request.path)
    else:
        return render_to_response('gourmetfeeds/welcome.html')
