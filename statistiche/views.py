# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from persone.models import *
from get2.calendario.models import *
from django.shortcuts import render_to_response, redirect, render
import calendar,datetime,locale
from django.db.models import Q, Count, Sum
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from statistiche.models import FiltroStatistiche
import pdb

#### inizio statistiche ####
elenco_statistiche=("Turni totali",
				"Punteggi totali",
			)

@login_required
def statistiche(request):
	#se l' intervallo non e specificato prendo tutto
	tot_turni, tot_punti, tot_turni_dipendenti, tot_punti_dipendenti = statistiche_intervallo(request)
	return render(request,'statistiche.html',{'tot_turni': tot_turni,'tot_punti': tot_punti, 'tot_punti_dipendenti':tot_punti_dipendenti,'tot_turni_dipendenti':tot_turni_dipendenti, 'FiltroStatistiche':FiltroStatistiche() ,'request':request})

import operator
from dateutil.relativedelta import relativedelta

def statistiche_intervallo(request, inizio = datetime.datetime(datetime.datetime.now().year , 1 , 1 ), fine = datetime.datetime.now().date() + datetime.timedelta( days=1 ), mansioni = Mansione.objects.all(), gruppi = Gruppo.objects.all(), tipi_turno = TipoTurno.objectsGet.all(), senza_gruppo = True):
	tot_turni = []
	tot_punti = []
	tot_turni_dipendenti = []
	tot_punti_dipendenti = []
	#Turno.objects.earliest(field_name='inizio')
	if getattr(settings, 'GET_DISTINGUI_DIPENDENTI', False):
		persone = Persona.objectsGet.filter(dipendente=False)
		dipendenti = Persona.objectsGet.filter(dipendente=True)
	else:
		persone = Persona.objectsGet.all()
		dipendenti = []

	if senza_gruppo:
		persone = persone.exclude(componenti_gruppo__escludi_stat=True).filter(Q(Q(componenti_gruppo__isnull=True) | Q(componenti_gruppo__in=gruppi))).distinct().values('id','nome','cognome')
		if getattr(settings, 'GET_DISTINGUI_DIPENDENTI', False):
			dipendenti = dipendenti.exclude(componenti_gruppo__escludi_stat=True).filter(Q(Q(componenti_gruppo__isnull=True) | Q(componenti_gruppo__in=gruppi))).distinct().values('id','nome','cognome')
	else:
		persone = persone.objectsGet.exclude(componenti_gruppo__escludi_stat=True).filter(componenti_gruppo__in=gruppi).values('id','nome','cognome')
		if getattr(settings, 'GET_DISTINGUI_DIPENDENTI', False):
			dipendenti = dipendenti.exclude(componenti_gruppo__escludi_stat=True).filter(componenti_gruppo__in=gruppi).values('id','nome','cognome')
	
	for p in persone:
		disp = Disponibilita.objects.values('turno__valore','punteggio').filter(persona_id = p["id"], tipo = "Disponibile", turno__inizio__gte=inizio, turno__fine__lte=fine, turno__tipo__in=tipi_turno ,mansione__in=mansioni.exclude(escludi_stat=True))
		p['tot_turni'] = disp.count()
		p['tot_punti'] = 0
		for d in disp:
			if getattr(settings, 'GET_SOVRASCRIVI_PUNTEGGIO', False) and d['punteggio'] != -1:
				p['tot_punti'] += d['punteggio']
			else:
				p['tot_punti'] += d['turno__valore']
		tot_turni.append(p)
		tot_punti.append(p)

	if getattr(settings, 'GET_DISTINGUI_DIPENDENTI', False):
		for p in dipendenti:
			disp = Disponibilita.objects.values('turno__valore','punteggio').filter(persona_id = p["id"], tipo = "Disponibile", turno__inizio__gte=inizio, turno__fine__lte=fine, turno__tipo__in=tipi_turno ,mansione__in=mansioni.exclude(escludi_stat=True))
			p['tot_turni'] = disp.count()
			p['tot_punti'] = 0
			for d in disp:
				if getattr(settings, 'GET_SOVRASCRIVI_PUNTEGGIO', False) and d['punteggio'] != -1:
					p['tot_punti'] += d['punteggio']
				else:
					p['tot_punti'] += d['turno__valore']
			tot_turni_dipendenti.append(p)
			tot_punti_dipendenti.append(p)
	#import pdb; pdb.set_trace()
	tot_turni.sort(key=operator.itemgetter('tot_turni'), reverse=True)
	tot_punti.sort(key=operator.itemgetter('tot_punti'), reverse=True)
	tot_turni_dipendenti.sort(key=operator.itemgetter('tot_turni'), reverse=True)
	tot_punti_dipendenti.sort(key=operator.itemgetter('tot_punti'), reverse=True)
	return tot_turni, tot_punti, tot_turni_dipendenti, tot_punti_dipendenti
#### fine statistiche ####