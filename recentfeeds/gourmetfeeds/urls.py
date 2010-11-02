from django.conf.urls.defaults import patterns, url

# Main application related URLs
urlpatterns = patterns('gourmetfeeds.views',
                       url(r'^$', 'welcome', name='gourmetfeeds_welcome'),
                       url(r'feeds/$', 'feeds', name='gourmetfeeds_feeds'),
)

# Account management URLs
urlpatterns += patterns('django.contrib.auth.views',
                       url(r'^login/$', 'login', name='login'),
                       url(r'^logout/$',
                           'logout',
                           {'next_page': '/gourmetfeeds/'},
                           name='logout'),
)
