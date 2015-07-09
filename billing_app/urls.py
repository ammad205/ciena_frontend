from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ngn_grid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^billing', 'billing_app.views.billing', name='billing'),

#    url(r'^admin/', include(admin.site.urls)),
)
