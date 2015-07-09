from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ngn_grid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^postMsg', 'pubsub_infra.views.postMessage', name='postMsg'),

#    url(r'^admin/', include(admin.site.urls)),
)
