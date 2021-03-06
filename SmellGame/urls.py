﻿#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
               url(r'^smellguess/',  include('SmellGuess.urls')),
               url(r'^smellgalaxy/', include('SmellGalaxy.urls')),
               url(r'^smellgift/',   include('SmellGift.urls')),
               url(r'^smelladmin/',  include('SmellAdmin.urls')),
               url(r'^admin/',       include(admin.site.urls)),
               url(r'^i18n/',        include('django.conf.urls.i18n')),
               url(r'^$',            lambda r : HttpResponseRedirect('smellguess/home/')),
               
]


# For the register application
# urlpatterns += patterns('SmellGame.register.views',
#                        url(r'^contact$', 'contact', name='contact'),
# )
