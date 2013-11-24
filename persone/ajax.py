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