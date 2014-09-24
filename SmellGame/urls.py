﻿#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
               url(r'^smellguess/',  include('SmellGuess.urls')),
               url(r'^smellgalaxy/', include('SmellGalaxy.urls')),
               url(r'^admin/',       include(admin.site.urls)),
               url(r'^home/',        'SmellGuess.views.homeView', name='home'),
]


# For the register application
# urlpatterns += patterns('SmellGame.register.views',
#                        url(r'^contact$', 'contact', name='contact'),
# )
