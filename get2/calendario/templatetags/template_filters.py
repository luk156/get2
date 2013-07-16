#template_filters.py
import pdb
from django import template
register = template.Library()
from get2.calendario.views import *
from django.forms.models import model_to_dict



@register.filter
def verifica_requisito(instance, arg):
	#pdb.set_trace()
	return instance.verifica_requisito(arg)
# template usage
#{{ instance|verifica_requisito:"value1" }}

@register.filter
def gia_disponibili(instance, arg):
	#pdb.set_trace()
	return instance.gia_disponibili(arg)

@register.filter
def gia_disponibile(instance, arg):
	if instance.persona_disponibilita.filter(turno=arg,tipo="Disponibile"):
		return instance.persona_disponibilita.filter(turno=arg,tipo="Disponibile")[0].id
	return False

@register.filter
def occorrenze(instance, arg):
	return Turno.objects.filter(occorrenza=arg)

@register.filter
def turno_futuro(instance):
	return instance.inizio>datetime.datetime.now()

@register.filter
def turno_intervallo_disponibilita(instance, arg):
	return verifica_intervallo(instance, arg)[0]
	
@register.filter
def errore_turno_intervallo_disponibilita(instance, arg):
	return verifica_intervallo(instance, arg)[1]
	
@register.filter
def stampa_requisito(instance):
	s=""
	r_as_dict = model_to_dict(instance)
	f=RequisitoForm(r_as_dict)
	if f.is_valid():
		for campo in f.fields.keys():
			val=str(f.cleaned_data[campo])
			if val=="True":
				val="<i class='icon-check'></i> "
			elif val=="False":
				val="<i class='icon-check-empty'></i> "
			s+='<td data-title='+str(campo)+'>'+val+'</td>'
		s+='<td><div class="btn-group superuser"><a class="btn dropdown-toggle btn-small" data-toggle="dropdown" href="#"><i class="icon-cog"></i> Azioni <span class="caret"></span></a><ul class="dropdown-menu pull-right"><li><a href="/impostazioni/requisito/modifica/'+str(instance.id)+'/"><i class="icon-edit"></i> modifica</a></li><li><a href="/impostazioni/requisito/elimina/'+str(instance.id)+'/"><i class="icon-trash"></i> elimina</a></li></ul></div></td>'
	return s
stampa_requisito.is_safe = True

@register.filter
def data_festa(instance):
	class_data=''
	if festivo(instance):
		class_data='festivo'
	elif prefestivo(instance):
		class_data='prefestivo'
	return class_data

@register.filter
def mansioni_indisp(instance, arg):
	#return "ciao"
	return instance.mansioni_indisponibili(arg)