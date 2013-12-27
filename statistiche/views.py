# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from persone.models import *
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
	dati=statistiche_intervallo(request)
	return render(request,'statistiche.html',{'dati': dati,'elenco_statistiche':elenco_statistiche,'FiltroStatistiche':FiltroStatistiche() ,'request':request})

from dateutil.relativedelta import relativedelta

def statistiche_intervallo(request, inizio = datetime.date(datetime.datetime.today().year,1,1), fine = datetime.datetime.now().date(), mansioni = Mansione.objects.all(), gruppi = Gruppo.objects.all(), senza_gruppo = True):
	#la funzione calcola le statistiche tra due date, rihiede 2 oggetti datetime.date
	dati=[]
	dati.append(elenco_statistiche)
	stat=[]
	if senza_gruppo:
		persone=Persona.objects.filter(Q(Q(componenti_gruppo__isnull=True) | Q(componenti_gruppo__in=gruppi))).distinct()
		print persone.query
		stat.append(persone.filter(persona_disponibilita__tipo="Disponibile", persona_disponibilita__mansione__in=mansioni, persona_disponibilita__turno__inizio__gte=inizio, persona_disponibilita__turno__fine__lte=fine ).annotate(tot_turni=Count('persona_disponibilita', distinct=True)).order_by("-tot_turni"))
		stat.append(persone.filter(persona_disponibilita__tipo="Disponibile", persona_disponibilita__mansione__in=mansioni, persona_disponibilita__turno__inizio__gte=inizio, persona_disponibilita__turno__fine__lte=fine ).annotate(tot_punti=Sum('persona_disponibilita__turno__valore')).order_by("-tot_punti"))
	else:
		stat.append(Persona.objects.filter(componenti_gruppo__in=gruppi,persona_disponibilita__tipo="Disponibile", persona_disponibilita__mansione__in=mansioni, persona_disponibilita__turno__inizio__gte=inizio, persona_disponibilita__turno__fine__lte=fine ).annotate(tot_turni=Count('persona_disponibilita', distinct=True)).order_by("-tot_turni"))
		stat.append(Persona.objects.filter(componenti_gruppo__in=gruppi,persona_disponibilita__tipo="Disponibile", persona_disponibilita__mansione__in=mansioni, persona_disponibilita__turno__inizio__gte=inizio, persona_disponibilita__turno__fine__lte=fine ).annotate(tot_punti=Sum('persona_disponibilita__turno__valore', distinct=True)).order_by("-tot_punti"))
	#pdb.set_trace()
	dati.append(stat)
	dati=zip(*dati)
	#risp=Persona.objects.filter(persona_disponibilita__tipo="Disponibile").annotate(tot_turni=Count('persona_disponibilita'))
	return dati


#### fine statistiche ####