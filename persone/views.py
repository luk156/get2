# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from get2.calendario.models import Disponibilita,Mansione
from persone.models import *
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

import csv, codecs
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import redirect_to_login
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from dateutil.relativedelta import relativedelta

def export_csv(request, queryset, export_data, filter_by=None, file_name='exported_data.csv',
        object_id=None, not_available='n.a.', require_permission=None):
    if require_permission and not (request.user.is_authenticated() and
                       request.user.has_perm(require_permission)):
        return redirect_to_login(request.path)
    queryset = queryset._clone()
    if filter_by and object_id:
        queryset = queryset.filter(**{'%s' % filter_by: object_id})

    def get_attr(object, attrs=None):
        if attrs == None or attrs == []:
            return object
        current = attrs.pop(0)
        try:
            return get_attr(callable(getattr(object, current)) and
                        getattr(object, current)() or
                        getattr(object, current), attrs)
        except (ObjectDoesNotExist, AttributeError):
            return not_available

    def stream_csv(data):
        sio = StringIO()
        writer = csv.writer(sio)
        writer.writerow(data)
        return sio.getvalue()

    def streaming_response_generator():
        yield codecs.BOM_UTF8
        yield stream_csv(zip(*export_data)[0])
        import django.db.models.query
        for item in queryset.iterator():

            row = []
            for attr in zip(*export_data)[1]:
                obj = get_attr(item, attr.split('.'))
                #pdb.set_trace()
                if callable(obj):
                    res = obj()
                else:
                    res = obj
                if isinstance(res, unicode) is True:
                    res = res.encode('utf-8')
                elif isinstance(res, datetime.date) or isinstance(res, datetime.datetime):
                	res=res.__str__()
                elif isinstance(res, django.db.models.query.QuerySet) is True:
                	elenco=''
                	for i in res:
                		elenco+=i.__unicode__()+", "
                	res=elenco
                elif isinstance(res, str) is False:
                    res = str(res)
                row.append(res)
            yield stream_csv(row)

    rsp = HttpResponse(streaming_response_generator(),
                        mimetype='text/csv',
                        content_type='text/csv; charset=utf-8')
    filename = object_id and callable(file_name) and file_name(object_id) or file_name
    rsp['Content-Disposition'] = 'attachment; filename=%s' % filename.encode('utf-8')
    return rsp




####   persona   ####
@user_passes_test(lambda u:u.is_staff)
def export_persona(request):
    # Create the HttpResponse object with the appropriate CSV header
    return export_csv(request, Persona.objects.all(), [('nome','nome'),
    	('cognome','cognome'),
    	('E-mail','user.email'),
    	('indirizzo','indirizzo'),
    	('nascita','nascita'),
    	('tel1','tel1'),
    	('tel2','tel2'),
    	('stato','stato'),
    	('competenze','competenze.all'),
    	('note','note'),
    	])

@user_passes_test(lambda u:u.is_staff)
def elenco_persona(request):
	#if request.user.is_staff:
	persone = Persona.objects.all().order_by('cognome')
	gruppi = Gruppo.objects.all()
	mansioni = Mansione.objects.all()
	risposta = HttpResponse(render(request,'elenco_persona.html',{'persone':persone,'stati':STATI,'request':request,'gruppi':gruppi,'mansioni':mansioni}))
	return risposta
	#else:
	#	return render(request,'staff-no.html')

@user_passes_test(lambda u:u.is_staff)
def nuovo_persona(request):
	#if request.user.is_staff:
	azione = 'nuovo'
	if request.method == 'POST':
		form = PersonaForm(request.POST)
		form.helper.form_action = '/persone/nuovo/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone')
	else:
		form = PersonaForm()
		form.helper.form_action = '/persone/nuovo/'
	return render(request,'form_persona.html',{'request':request,'form': form,'azione': azione,})
	#else:
	#	return render(request,'staff-no.html')

@user_passes_test(lambda u:u.is_staff)
def modifica_persona(request,persona_id):
	azione = 'modifica'
	per = Persona.objects.get(id=persona_id)
	if request.method == 'POST':  # If the form has been submitted...
		form = PersonaForm(request.POST, instance=per)  # necessario per modificare la riga preesistente
		form.helper.form_action = '/persone/modifica/'+str(per.id)+'/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone') # Redirect after POST
	else:
		form = PersonaForm(instance=per)
		form.helper.form_action = '/persone/modifica/'+str(per.id)+'/'
	return render(request,'form_persona.html',{'request': request, 'form': form,'azione': azione, 'per': per,'mansione_form':MansioneForm()})

@user_passes_test(lambda u: u.is_superuser)
def elimina_persona(request,persona_id):
	p=Persona.objects.get(id=persona_id)
	p.delete()
	return HttpResponseRedirect('/persone/')

@user_passes_test(lambda u:u.is_staff)
def nuovo_gruppo(request):
	#if request.user.is_staff:
	azione = 'nuovo'
	if request.method == 'POST':
		form = GruppoForm(request.POST)
		form.helper.form_action = '/persone/gruppo/nuovo/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone')
	else:
		form = GruppoForm()
		form.helper.form_action = '/persone/gruppo/nuovo/'
	return render(request,'form_gruppo.html',{'request':request,'form': form,'azione': azione,})
	#else:
	#	return render(request,'staff-no.html')

@user_passes_test(lambda u:u.is_staff)
def modifica_gruppo(request,gruppo_id):
	azione = 'modifica'
	g = Gruppo.objects.get(id=gruppo_id)
	if request.method == 'POST':  # If the form has been submitted...
		form = GruppoForm(request.POST, instance=g)  # necessario per modificare la riga preesistente
		form.helper.form_action = '/persone/gruppo/modifica/'+str(g.id)+'/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone') # Redirect after POST
	else:
		form = GruppoForm(instance=g)
		form.helper.form_action = '/persone/gruppo/modifica/'+str(g.id)+'/'
	return render(request,'form_gruppo.html',{'request': request, 'form': form,'azione': azione, 'g': g,})

@user_passes_test(lambda u:u.is_staff)
def elimina_gruppo(request,gruppo_id):
	p=Gruppo.objects.get(id=gruppo_id)
	p.delete()
	return HttpResponseRedirect('/persone/')

@user_passes_test(lambda u:u.is_staff)
def gruppoaggiungi(request, gruppo_id, per_id):
	g=Gruppo.objects.get(id=gruppo_id)
	p=Persona.objects.get(id=per_id)
	g.componenti.add(v)
	g.save()
	return HttpResponseRedirect('/persone/')

@user_passes_test(lambda u:u.is_staff)
def aggiungilista(request,azione,arg,persone):
	for per_id in persone.rsplit('_'):
		if azione=='aggiungi_g':
			g=Gruppo.objects.get(id=arg)
			v=Persona.objects.get(id=per_id)
			g.componenti.add(v)
			g.save()
		elif azione=='aggiungi_m':
			m = Mansione.objects.get(id=arg)
			v=Persona.objects.get(id=per_id)
			v.competenze.add(m)
			v.save()
		elif azione=='rimuovi_g':
			g=Gruppo.objects.get(id=arg)
			v=Persona.objects.get(id=per_id)
			g.componenti.remove(v)
			g.save()
		elif azione=='rimuovi_m':
			m = Mansione.objects.get(id=arg)
			v=Persona.objects.get(id=per_id)
			v.competenze.remove(m)
			v.save()
	return HttpResponseRedirect('/persone/')

####   fine persona   ####

#### inizio pagina persona ####

from django.db.models import Q, Count, Sum

@login_required
def visualizza_persona(request,persona_id):
	persona = Persona.objects.get(id=persona_id)
	oggi = datetime.datetime.today()
	disponibilita = Disponibilita.objects.filter(persona=persona, tipo="Disponibile", turno__fine__lte=oggi).order_by('turno__inizio')
	try :
		start=disponibilita[:1].get().turno.inizio
	except:
		start=datetime.datetime.today()
	turni=[]
	mansioni=Mansione.objects.exclude(escludi_stat=True).filter(mansione_disponibilita__persona=persona,mansione_disponibilita__tipo="Disponibile", mansione_disponibilita__turno__fine__lte=oggi).annotate(parziale=Count('id'))
	tot_turni = disponibilita.count()
	tot_punti = 0
	for d in disponibilita:
			tot_punti += d.turno.valore
	while start < oggi:
		stop = start + relativedelta( months = +1 )
		n=disponibilita.filter(turno__inizio__gte=start, turno__fine__lte=stop).count()
		turni.append([start,n])
		start = stop
	#import pdb; pdb.set_trace()
	#print turni
	if request.user.is_staff or request.user.get_profile()==persona:
	  return render(request,'dettaglio_persona.html',{'request': request, 'turni': turni, 'mansioni': mansioni ,'persona': persona, 'tot_punti': tot_punti, 'tot_turni': tot_turni})

#### fine pagina persona ####