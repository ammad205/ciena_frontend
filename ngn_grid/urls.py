from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ngn_grid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^connect/$', 'ngn_grid.views.connect'),
    url(r'^connect2/$', 'ngn_grid.views.connect2'),
    url(r'^ammad/$', 'ngn_grid.views.ammad'),
    url(r'^ammad2/$', 'ngn_grid.views.ammad2'),
    url(r'^spawn/$', 'ngn_grid.views.spawn'),
    url(r'^$', 'ngn_grid.views.login', name='index'),
    url(r'^login', 'ngn_grid.views.login_user', name='login'),
    url(r'^logout', 'ngn_grid.views.logout', name='logout'),
    url(r'^dashboard', 'ngn_grid.views.index', name='dashboard'),
    url(r'^panel', 'ngn_grid.views.panel', name='panel'),
    url(r'^authentication', 'ngn_grid.views.authentication', name='authentication'),
    url(r'^create_user', 'ngn_grid.views.create_user', name='create_user'),
    url(r'^nfvo/', include('nfvo_app.urls')),
    url(r'^analytics/', include('analytics_app.urls')),
    url(r'^billing/', include('billing_app.urls')),
    url(r'^logs/', include('logs_app.urls')),

#    url(r'^admin/', include(admin.site.urls)),
)
