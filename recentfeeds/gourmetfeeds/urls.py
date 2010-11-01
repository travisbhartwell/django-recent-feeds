from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
                       (r'^$', 'gourmetfeeds.views.welcome'),
                       (r'^login/$', 'django.contrib.auth.views.login'),
)
