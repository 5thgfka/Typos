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
    url(r'typo/(?P<typoid>.*)$', 'typos.views.typo', name='typo'),
    # user
    url(r'userStatics/(?P<userid>.*)$', 'typos.views.userStatics', name='userStatics'),
    # rank
    url(r'rank/$', 'typos.views.rank', name='rank'),
    # notice
    url(r'notice/$', 'typos.views.notice', name='notice'),
    # accounts
    url(r'^accounts/login/$', 'accounts.helper.login', name='login'),
    url(r'^accounts/logout/$', 'accounts.helper.logout', name='logout'),
    url(r'^accounts/register/$', 'accounts.helper.register', name='register'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
    # check code
    url(r'^get_check_code_image/$', 'typos.views.getcci', name="getcci"),
    url(r'^getEarth/$', 'typos.views.getEarth', name="getEarth"),
)
