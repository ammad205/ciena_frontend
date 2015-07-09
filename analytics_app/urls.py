from django.conf.urls import patterns, include, url
from django.contrib import admin
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ngn_grid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'analytics.views.home', name='analyticshome'),
    url(r'^ajax/dashboard.html', 'analytics.views.dashboard', name='dashboard'),
    url(r'^testrun', 'analytics_app.views.testrun', name='testrun'),
    url(r'^analyticsDashboard', 'analytics_app.views.analyticsDashboard', name='analyticsDashboard'),
    url(r'^analytics', 'analytics_app.views.analytics', name='analytics'),
    #url(r'^getlast24hours', 'analytics_app.views.getlast24hours', name='getlast24hours'),
    url(r'^requestAuthToken', 'analytics_app.network_analytics.requestAuthToken', name='requestAuthToken'),
    url(r'^getVMUpTime', 'analytics_app.network_analytics.getVMUpTime', name='getVMUpTime'),
    url(r'^getlast24hoursIng', 'analytics_app.network_analytics.getlast24hoursIng', name='getlast24hoursIng'),
    url(r'^getlast24hoursEg', 'analytics_app.network_analytics.getlast24hoursEg', name='getlast24hoursEg'),
    url(r'^getVMStats/*', 'analytics_app.network_analytics.getVMStats', name='getVMStats'),
    url(r'^getNetworkStats/NetworkDataUsage/*', 'analytics_app.network_analytics.getNetworkDataUsage', name='getNetworkDataUsage'),
    url(r'^getNetworkStats/NetworkBandwidthUsage/*', 'analytics_app.network_analytics.getNetworkBandwidthUsage', name='getNetworkBandwidthUsage'),
    url(r'^getNetworkStats/NetworkFlowCount/*', 'analytics_app.network_analytics.getNetworkFlowCount', name='getNetworkFlowCount'),
    url(r'^getNetworkStats/NetworkPacketCount/*', 'analytics_app.network_analytics.getNetworkPacketCount', name='getNetworkPacketCount'),
    url(r'^getNetworkStats/*', 'analytics_app.network_analytics.getNetworkStats', name='getNetworkStats'),
    url(r'^', 'analytics_app.views.generic', name="forwarder"),


#    url(r'^admin/', include(admin.site.urls)),
)
