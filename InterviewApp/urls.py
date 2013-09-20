from django.conf.urls import patterns, include, url
import SampleISP.urls
from InterviewApp import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# url patterns for project site-wide
urlpatterns = patterns('',
    url(r'^$', 'InterviewApp.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Include SampleISP urls
    url(r'^', include(SampleISP.urls, namespace='SampleISP')),
)

