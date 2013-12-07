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

@login_required
def statistiche(request):
	#se l' intervallo non e specificato prendo tutto
	persone, serie_tot_turni=statistiche_intervallo(request)
	return render(request,'statistiche.html',{'persone': persone, 'serie_tot_turni': serie_tot_turni,'FiltroStatistiche':FiltroStatistiche() ,'request':request})

from dateutil.relativedelta import relativedelta

def statistiche_intervallo(request, inizio = datetime.date(datetime.datetime.today().year,1,1), fine = datetime.datetime.now().date(), mansioni = Mansione.objects.all(), gruppi = Gruppo.objects.all(), senza_gruppo = True):
	if senza_gruppo:
		persone=Persona.objects.filter(Q(Q(componenti_gruppo__isnull=True) | Q(componenti_gruppo__in=gruppi)))
	else:
		persone=Persona.objects.filter(componenti_gruppo__in=gruppi)
	serie_tot_turni = []
	for mansione in mansioni:
		tot_turni_persona_mansione=[]
		for persona in persone:
			tot_turni_persona_mansione.append(Disponibilita.objects.filter(tipo="Disponibile",mansione=mansione,persona=persona,turno__inizio__gte=inizio, turno__fine__lte=fine).count())
		serie_tot_turni.append([mansione,tot_turni_persona_mansione])
	return persone, serie_tot_turni

#### fine statistiche ####