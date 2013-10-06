# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from persone.models import *
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
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
    	('retraining','retraining'),
    	('retraining_blsd','retraining_blsd'),
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
	g.save
	return HttpResponseRedirect('/persone/')

@user_passes_test(lambda u:u.is_staff)
def aggiungilista(request,azione,arg,persone):
	for per_id in persone.rsplit('_'):
		if azione=='aggiungi_g':
			g=Gruppo.objects.get(id=arg)
			v=Persona.objects.get(id=per_id)
			g.componenti.add(v)
			g.save
		elif azione=='aggiungi_m':
			m = Mansione.objects.get(id=arg)
			v=Persona.objects.get(id=per_id)
			v.competenze.add(m)
			v.save
		elif azione=='rimuovi_g':
			g=Gruppo.objects.get(id=arg)
			v=Persona.objects.get(id=per_id)
			g.componenti.remove(v)
			g.save
		elif azione=='rimuovi_m':
			m = Mansione.objects.get(id=arg)
			v=Persona.objects.get(id=per_id)
			v.competenze.remove(m)
			v.save
	return HttpResponseRedirect('/persone/')

####   fine persona   ####

#### inizio pagina persona ####
@login_required
def visualizza_persona(request,persona_id):
	persona = Persona.objects.get(id=persona_id)
	if request.user.is_staff or request.user.get_profile()==persona:
	  return render(request,'dettaglio_persona.html',{'request': request, 'persona': persona})

#### fine pagina persona ####