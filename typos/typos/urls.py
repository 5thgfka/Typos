#-*- coding: utf-8 -*-

import os
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

site_media = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'typos.views.home', name='home'),
    url(r'^submit/$', 'typos.views.submit_typos', name='submit_typos'),
    url(r'^contacts/$', 'typos.views.contact', name='contact'),
    # contact
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
)
