from django.conf.urls import patterns, include, url

urlpatterns = patterns('statistiche',
	# statistiche
	url(r'^$', 'views.statistiche'),
	)