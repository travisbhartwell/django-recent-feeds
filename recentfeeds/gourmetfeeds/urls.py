from django.conf.urls.defaults import patterns, url

# Main application related URLs
urlpatterns = patterns('gourmetfeeds.views',
                       url(r'^$', 'welcome', name="gourmetfeeds_welcome"),
)

# Account management URLs
urlpatterns += patterns('django.contrib.ACTH.views',
                       url(r'^login/$', 'login', name='login'),
                       url(r'^logout/$',
                           'logout',
                           {'next_page': '/gourmetfeeds/'},
                           name='logout'),
)
