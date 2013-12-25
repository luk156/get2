from django.conf.urls import *
from django.views.generic import TemplateView
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    # statistiche
    url(r'^statistiche/', include('statistiche.urls')),
    url(r'^persone/', include('persone.urls')),
    #url(r'^gestione/', include('gestione.urls')),
)

urlpatterns += patterns('get2.calendario',
	# calendario
	(r'^$','views.home'),
	(r'^calendario/$', 'views.home'),
	(r'^touch/(?P<v>\w+)$', 'views.touch'),
	(r'^calendario/(?P<cal_id>\w+)/$', 'views.calendario'),
	(r'^stampa_calendario/(?P<cal_id>\w+)/$', 'views.stampa_calendario'),
	(r'^calendario/(?P<cal_id>\w+)/(?P<azione>\w+)$', 'views.calendarioazione'),
	# utenti
	(r'^utenti/$', 'views.elenco_utente'),
	(r'^utenti/nuovo/$', 'views.nuovo_utente'),
	(r'^utenti/modifica/(?P<utente_id>\w+)/password/$', 'views.modifica_password_utente'),
	(r'^utenti/modifica/(?P<utente_id>\w+)/password_personale/$', 'views.modifica_password_personale'),
	(r'^utenti/modifica/(?P<utente_id>\w+)/$', 'views.modifica_utente'),
	(r'^utenti/elimina/(?P<utente_id>\w+)/$', 'views.elimina_utente'),
	# mansioni
	(r'^impostazioni/mansione/nuovo/(?P<padre_id>\w+)/$', 'views.nuovo_mansione'),
	(r'^impostazioni/mansione/modifica/(?P<mansione_id>\w+)/$', 'views.modifica_mansione'),
	(r'^impostazioni/mansione/elimina/(?P<mansione_id>\w+)/$', 'views.elimina_mansione'),
	# turno
	(r'^turno/(?P<cal_id>\w+)/nuovo/$', 'views.nuovo_turno'),
	(r'^turno/modifica/(?P<turno_id>\w+)/$', 'views.modifica_turno'),
	(r'^turno/elimina/(?P<turno_id>\w+)/$', 'views.elimina_turno'),
	(r'^turno/elimina_occorrenza/(?P<occorrenza_id>\w+)/$', 'views.elimina_turno_occorrenza_succ'),
	(r'^turno/elimina_occorrenza_tot/(?P<occorrenza_id>\w+)/$', 'views.elimina_turno_occorrenza'),
	(r'^cerca_persona/(?P<turno_id>\w+)/(?P<mansione_id>\w+)', 'views.cerca_persona'),
	(r'^disponibilita/(?P<turno_id>\w+)/(?P<mansione_id>\w+)/(?P<persona_id>\w+)/(?P<disponibilita>\w+)', 'views.disponibilita_url'),
	(r'^rimuovi_disponibilita/(?P<disp_id>\w+)', 'views.rimuovi_disponibilita'),
	(r'^disponibilita_gruppo/(?P<turno_id>\w+)/(?P<gruppo_id>\w+)/', 'views.disponibilita_gruppo'),
	#(r'^turno/cerca_persona/(?P<turno_id>\w+)/(?P<mansione_id>\w+)/$', 'views.turno_cerca'),
	# impostazioni
	(r'^impostazioni/$', 'views.impostazioni'),
	(r'^impostazioni/calendario/nuovo/$', 'views.nuovo_calendario'),
	(r'^impostazioni/calendario/modifica/(?P<cal_id>\w+)/$', 'views.modifica_calendario'),
	(r'^impostazioni/calendario/elimina/(?P<cal_id>\w+)/$', 'views.elimina_calendario'),
	(r'^impostazioni/tipo_turno/nuovo/$', 'views.nuovo_tipo_turno'),
	(r'^impostazioni/tipo_turno/modifica/(?P<tipo_turno_id>\w+)/$', 'views.modifica_tipo_turno'),
	(r'^impostazioni/tipo_turno/elimina/(?P<tipo_turno_id>\w+)/$', 'views.elimina_tipo_turno'),
	(r'^impostazioni/tipo_turno/aggiungi_requisito/(?P<tipo_turno_id>\w+)/$', 'views.nuovo_requisito'),
	(r'^impostazioni/requisito/modifica/(?P<requisito_id>\w+)/$', 'views.modifica_requisito'),
	(r'^impostazioni/requisito/elimina/(?P<requisito_id>\w+)/$', 'views.elimina_requisito'),
	(r'^impostazioni/notifica/nuovo/$', 'views.nuovo_impostazioni_notifica'),
	(r'^impostazioni/notifica/modifica/(?P<impostazioni_notifica_id>\w+)/$', 'views.modifica_impostazioni_notifica'),
	(r'^impostazioni/notifica/elimina/(?P<impostazioni_notifica_id>\w+)/$', 'views.elimina_impostazioni_notifica'),
	# notifiche
   	(r'^notifiche/$', 'views.elenco_notifica'),
   	(r'^notifiche/elimina/(?P<notifica_id>\w+)/$', 'views.elimina_notifica'),
)

urlpatterns += patterns('django.contrib.auth.views',
    #utente
    #(r'^utente/nuovo/$', 'turni.views.nuovoutente'),
    (r'^utenti/reset/$', 'password_reset'),
    (r'^utenti/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'^utenti/reset/completa/$', 'password_reset_complete'),
    (r'^utenti/reset/ok/$', 'password_reset_done'),
    )

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name':'registration/login.html'} ),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    )

#urlpatterns = patterns('',
#    url(r'', include('gcm.urls')),
#)