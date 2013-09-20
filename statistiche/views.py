# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
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

import pdb

#### inizio statistiche ####
elenco_statistiche=("Turni totali",
				"Punteggi totali",
			)

@login_required
def statistiche(request):
	#se l' intervallo non e specificato prendo tutto
	dati=statistiche_intervallo(request,datetime.date(2000,1,1),datetime.datetime.now().date())
	return render(request,'statistiche.html',{'dati': dati,'elenco_statistiche':elenco_statistiche,'request':request})

from dateutil.relativedelta import relativedelta

def statistiche_intervallo(request, inizio, fine):
	#la funzione calcola le statistiche tra due date, rihiede 2 oggetti datetime.date
	dati=[]
	dati.append(elenco_statistiche)
	stat=[]
	stat.append(Persona.objects.filter(persona_disponibilita__tipo="Disponibile", persona_disponibilita__turno__inizio__gte=inizio, persona_disponibilita__turno__fine__lte=fine ).annotate(tot_turni=Count('persona_disponibilita')).order_by("-tot_turni"))
	stat.append(Persona.objects.filter(persona_disponibilita__tipo="Disponibile", persona_disponibilita__turno__inizio__gte=inizio, persona_disponibilita__turno__fine__lte=fine ).annotate(tot_punti=Sum('persona_disponibilita__turno__valore')).order_by("-tot_punti"))
	#pdb.set_trace()
	dati.append(stat)
	dati=zip(*dati)
	#risp=Persona.objects.filter(persona_disponibilita__tipo="Disponibile").annotate(tot_turni=Count('persona_disponibilita'))
	return dati


#### fine statistiche ####