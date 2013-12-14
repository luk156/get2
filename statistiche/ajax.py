from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from statistiche.models import *
from persone.models import *
from statistiche.views import *
from dajaxice.utils import deserialize_form
from django.template.loader import render_to_string
from django.template import Context, Template

@dajaxice_register
def aggiorna_statistiche(request,da,al,mansioni,gruppi):
        dajax=Dajax()
        elenco_mansioni=Mansione.objects.filter(id__in=mansioni.rsplit('_'))
        senza_gruppo=False
        #import pdb; pdb.set_trace()
        if "all_" in gruppi:
                senza_gruppo=True
                gruppi=gruppi.replace("all_","")
        if "all" in gruppi:
                senza_gruppo=True
                gruppi=gruppi.replace("all","")
        if gruppi != "":
                elenco_gruppi=Gruppo.objects.filter(id__in=gruppi.rsplit('_'))
        else:
                elenco_gruppi=Gruppo.objects.all()

        data_da=datetime.date(2000,1,1)
        data_al=datetime.datetime.now().date()
        if (da=="0"):
                elenco_masnioni=Mansione.objects.all()
                elenco_gruppi=Gruppo.objects.all()
        elif (da!="" and al!=""):
                data_da=datetime.datetime.strptime(da, "%d/%m/%Y").date()
                data_al=datetime.datetime.strptime(al, "%d/%m/%Y").date()
        dati=statistiche_intervallo(request,data_da,data_al,elenco_mansioni,elenco_gruppi,senza_gruppo)
        html_statistiche = render_to_string( 'statistiche/statistiche.html', { 'dati': dati, 'elenco_statistiche': elenco_statistiche, 'request':request } )
        dajax.assign('div #stat', 'innerHTML', html_statistiche)
        dajax.script("$('#loading').addClass('hidden');")
        return dajax.json()