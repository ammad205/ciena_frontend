from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ngn_grid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^nfvHom', 'nfvo_app.views.nfvHome', name='nfvHome'),
    url(r'^nfvIndex', 'nfvo_app.views.nfvIndex', name='nfvIndex'),
    url(r'^nfvPanel', 'nfvo_app.views.nfvPanel', name='nfvPanel'),
    url(r'^policyBuilder', 'nfvo_app.views.policyBuilder', name='policyBuilder'),
    url(r'^nfvActiveTopology', 'nfvo_app.views.nfvActiveTopology', name='nfvActiveTopology'),
    url(r'^nfvDropBox', 'nfvo_app.views.nfvDropBox', name='nfvDropBox'),
    url(r'^spawnModeler', 'nfvo_app.views.spawnModeler', name='spawnModeler'),
    url(r'^userHistory', 'nfvo_app.views.userHistory', name='userHistory'),
    url(r'^allData', 'nfvo_app.views.userHistoryData', name='allData'),
    url(r'^showUserData', 'nfvo_app.views.showUserData', name='showUserData'),
    url(r'^deleteUserData', 'nfvo_app.views.deleteUserData', name='deleteUserData'),
    url(r'^serviceMonitoring', 'nfvo_app.views.serviceMonitoring', name='serviceMonitoring'),
    url(r'^PB', 'nfvo_app.views.PB'),
    url(r'^processTest', 'nfvo_app.views.processTest', name='processTest'),
    url(r'^diagnostic', 'nfvo_app.views.diagnostic', name='diagnostic'),
    url(r'^deleteOpenstackVM', 'nfvo_app.views.deleteOpenstackVM', name='deleteOpenstackVM'),
    url(r'^queue', 'nfvo_app.views.queue', name='queue'),

    url(r'^n2fvHom', 'nfvo_app.views.n2fvHome'),

    #url(r'^admin/', include(admin.site.urls)),
)

