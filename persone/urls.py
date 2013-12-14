from django.conf.urls import patterns, include, url

urlpatterns = patterns('persone',
	# persone
	(r'^$', 'views.elenco_persona'),
	(r'^export/$', 'views.export_persona'),
	(r'^nuovo/$', 'views.nuovo_persona'),
	(r'^modifica/(?P<persona_id>\w+)/$', 'views.modifica_persona'),
	(r'^visualizza/(?P<persona_id>\w+)/$', 'views.visualizza_persona'),
	(r'^elimina/(?P<persona_id>\w+)/$', 'views.elimina_persona'),
	(r'^aggiungilista/(?P<azione>\w+)/(?P<arg>\w+)/(?P<persone>\w+)/$', 'views.aggiungilista'),
	(r'^gruppo/nuovo/$', 'views.nuovo_gruppo'),
	(r'^gruppo/modifica/(?P<gruppo_id>\w+)/$', 'views.modifica_gruppo'),
	(r'^gruppo/elimina/(?P<gruppo_id>\w+)/$', 'views.elimina_gruppo'),	
	)

