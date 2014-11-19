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
    url(r'^exitstream$', 'liveStreaming.views.exit')
)
