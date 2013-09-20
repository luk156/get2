from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from get2.calendario.models import *
from get2.calendario.views import *
from django.template.loader import render_to_string
import pdb

@dajaxice_register
def aggiorna_statistiche(request,da,al):
	dajax=Dajax()
	if (da=="0"):
		dati=statistiche_intervallo(request,datetime.date(2000,1,1),datetime.datetime.now().date())
		html_statistiche = render_to_string( 'statistiche.html', { 'dati': dati, 'elenco_statistiche': elenco_statistiche, 'request':request } )
		dajax.assign('div #stat', 'innerHTML', html_statistiche)
	elif (da!="" and al!=""):
		data_da=datetime.datetime.strptime(da, "%d/%m/%Y").date()
		data_al=datetime.datetime.strptime(al, "%d/%m/%Y").date()
		dati=statistiche_intervallo(request,data_da,data_al)
		html_statistiche = render_to_string( 'statistiche.html', { 'dati': dati, 'elenco_statistiche': elenco_statistiche, 'request':request } )
		dajax.assign('div #stat', 'innerHTML', html_statistiche)
		dajax.script("$('#loading').addClass('hidden');")
		#dajax.alert()
	return dajax.json()