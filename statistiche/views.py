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
	tot_turni, tot_punti =statistiche_intervallo(request)
	return render(request,'statistiche.html',{'tot_turni': tot_turni,'tot_punti': tot_punti,'FiltroStatistiche':FiltroStatistiche() ,'request':request})

import operator
from dateutil.relativedelta import relativedelta

def statistiche_intervallo(request, inizio = datetime.datetime(datetime.datetime.now().year , 1 , 1 ), fine = datetime.datetime.now().date(), mansioni = Mansione.objects.all(), gruppi = Gruppo.objects.all(), senza_gruppo = True):
	tot_turni = []
	tot_punti = []
	#Turno.objects.earliest(field_name='inizio')
	if senza_gruppo:
		persone = Persona.objects.exclude(componenti_gruppo__escludi_stat=True).filter(Q(Q(componenti_gruppo__isnull=True) | Q(componenti_gruppo__in=gruppi))).distinct().values('id','nome','cognome')
		#print persone
	else:
		persone = Persona.objects.exclude(componenti_gruppo__escludi_stat=True).filter(componenti_gruppo__in=gruppi).values('id','nome','cognome')

	for p in persone:
		disp = Disponibilita.objects.values('turno__valore').filter(persona_id = p["id"], tipo = "Disponibile", turno__inizio__gte=inizio, turno__fine__lte=fine, mansione__in=mansioni.exclude(escludi_stat=True))
		p['tot_turni'] = disp.count()
		p['tot_punti'] = 0
		for d in disp:
			p['tot_punti'] += d['turno__valore']
		tot_turni.append(p)
		tot_punti.append(p)
	#import pdb; pdb.set_trace()
	tot_turni.sort(key=operator.itemgetter('tot_turni'), reverse=True)
	tot_punti.sort(key=operator.itemgetter('tot_punti'), reverse=True)
	return tot_turni, tot_punti
#### fine statistiche ####