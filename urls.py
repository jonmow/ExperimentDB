from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/(.*)', admin.site.root),
	(r'^accounts/login/', 'django.contrib.auth.views.login'),
	(r'^experiment/(?P<experimentID>[-\w]+)/$', 'experimentdb.data.views.experiment'),
	(r'^experiments?/$', 'experimentdb.data.views.index'),
	(r'^search/$', 'experimentdb.views.search'),
	(r'^projects?/(?P<project>[-\w]+)/$', 'experimentdb.projects.views.detail'),		
	(r'^projects?/$', 'experimentdb.projects.views.index'),
	(r'^subprojects?/(?P<subproject>[-\w]+)/$', 'experimentdb.projects.views.subproject_detail'),
	(r'^proteins?/(?P<protein>[-\w\d]+)/$', 'experimentdb.proteins.views.detail'),		
	(r'^proteins?/$', 'experimentdb.proteins.views.index'),
)