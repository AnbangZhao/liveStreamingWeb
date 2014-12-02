from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'liveStreaming.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #home page
    url(r'^$', 'liveStreaming.views.home'),
    #open streaming connection ffmpeg
    url(r'^openstream$', 'liveStreaming.views.open'),
    #exit streaming
    url(r'^exitstream$', 'liveStreaming.views.exit'),
    #degrade all stream resolutions
    url(r'^degrade$', 'liveStreaming.views.degrade'),
    #deal with no viewer situation
    url(r'^noviewer$', 'liveStreaming.views.noviewer'),
    #deal with errors
    url(r'^error$', 'liveStreaming.views.error'),
    #check if the stream exists
    url(r'^check$', 'liveStreaming.views.check'),
)
