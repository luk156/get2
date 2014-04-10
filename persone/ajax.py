from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from get2.calendario.models import *
from get2.calendario.views import *
from dajaxice.utils import deserialize_form
import pdb
from django.template.loader import render_to_string
from django.template import Context, Template

@dajaxice_register
def elimina_persona(request,persona_id):
	dajax = Dajax()
	if request.user.is_superuser:
            per=Persona.objects.get(id=persona_id)
            per.delete()
            dajax.remove('#persona-'+str(persona_id))
	dajax.script("$('#loading').addClass('hidden');")
	return dajax.json()

@dajaxice_register
def elimina_gruppo(request,gruppo_id):
	#pdb.set_trace()
	dajax = Dajax()
	if request.user.is_staff:
            gr=Gruppo.objects.get(id=gruppo_id)
            gr.delete()
            dajax.remove('#gruppo-'+str(gruppo_id))
	dajax.script("$('#loading').addClass('hidden');")
	return dajax.json()


@dajaxice_register
def persona_stato(request,stato,persona):
	dajax=Dajax()
	per=Persona.objects.get(id=persona)
	per.stato=stato
	per.save()
	dajax.script('$(".bottom-right").notify({ message: { text: "Modifiche apportate con successo" }}).show();')
	dajax.script("$('#loading').addClass('hidden');")
	return dajax.json()


@dajaxice_register
def elimina_persona_modal(request,persona_id):
    dajax=Dajax()
    p=Persona.objects.get(id=persona_id)
    html_elimina = render_to_string( 'persone/elimina_persona.html', { 'persona': p, 'request':request } )
    dajax.assign('div #elimina-persona-'+str(p.id), 'innerHTML', html_elimina)
    dajax.script("$('#elimina-persona-"+str(p.id)+"').modal('show');")
    return dajax.json() 

@dajaxice_register
def sync_misecampi(request):
    dajax=Dajax()
    from django.core.management import call_command
    #pdb.set_trace()
    call_command('MiseCampi')
    dajax.script("setInterval(function() {Dajaxice.persone.sync_misecampi_status(Dajax.process,{});}, 3000);")
    return dajax.json() 

@dajaxice_register
def sync_misecampi_status(request):
    dajax=Dajax()
    import MySQLdb
    #pdb.set_trace()
    database = settings.DATABASES['default']
    db = MySQLdb.connect(host=database['HOST'], user=database['USER'], passwd=database['PASSWORD'], db=database['NAME'])
    cur_my = db.cursor()
    cur_my.execute("SELECT * FROM sincronizza WHERE stato='INCORSO' ORDER BY data DESC LIMIT 1; ")
    last_sync = cur_my.fetchall()
    if len(last_sync) > 0:
        dajax.script("$('.box-header.persone > .btn-group > a', '#persone').html('Sincronizzaizone in corso ("+last_sync[0][3]+")').addClass('disabled')")
    else:
        dajax.script("$('.box-header.persone > .btn-group > a', '#persone').html('<i class=\"icon-refresh\"> </i> Sincronizza').removeClass('disabled')")
    return dajax.json() 