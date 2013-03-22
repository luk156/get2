#from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from get2.calendario.models import *
from get2.calendario.views import *
from dajaxice.utils import deserialize_form
import pdb
from django.template.loader import render_to_string

@dajaxice_register
def mansione_form(request, form):
    dajax = Dajax()
    form = MansioneForm(deserialize_form(form))
    if form.is_valid():
        i = form.save()
        dajax.script('$("#form_mansione" ).dialog("close");')
        #pdb.set_trace()
        html = '<option value="' + str(i.id) + '">' + str(i.descrizione) + '</option>'
        dajax.append('#id_competenze', 'innerHTML', html)
        #dajax.alert("aggiunto!")
    else:
        dajax.remove_css_class('#form_tipo_turno input', 'error')
        for error in form.errors:
            # error  il nome del campo
            dajax.add_css_class('#id_%s' % error, 'ui-state-error')
    return dajax.json()


@dajaxice_register
def elimina_persona(request,persona_id):
    per=Persona.objects.get(id=persona_id)
    per.delete()
    dajax = Dajax()
    dajax.remove('#persona-'+str(persona_id))
    return dajax.json()

@dajaxice_register
def elimina_utente(request,utente_id):
    user=User.objects.get(id=utente_id)
    dajax = Dajax()
    if (not user.is_staff() or request.user.is_superuser):
        #user.delete()
        dajax.remove('#utente-'+str(utente_id))
    else:
        pass
    return dajax.json()


@dajaxice_register
def utente_persona(request,user_id,persona_id):
    dajax = Dajax()
    s=''
    if Persona.objects.filter(user=user_id):
        a=User.objects.get(id=user_id)
        per=Persona.objects.get(user=user_id)
        per.user=None
        per.save()
        if persona_id=='n':
            s=s+'noty({"text":"l\' utente <b>'+str(a)+'</b> non e piu assegnato a <b>nessuna persona</b>","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});'
            pass

    if persona_id!='n' and User.objects.filter(pers_user=persona_id):
        a=User.objects.get(pers_user=persona_id)
        dajax.assign('select#'+str(a.id),'selectedIndex','0')
        s=s+'noty({"text":"<b>Attenzione</b>:La persona era precedentemente assegnato all\'utente <b>'+str(a)+'</b>","layout":"bottomRight","type":"alert","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});'

    if persona_id!='n':
        per=Persona.objects.get(id=persona_id)
        u=User.objects.get(id=user_id)
        per.user=u
        s=s+'noty({"text":"La persona <b>'+str(per)+'</b> e stato assegnata all\'utente <b>'+str(u)+'</b>","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});'

    dajax.script(s)
    per.save()
    return dajax.json()

@dajaxice_register
def utente_staff(request,user_id):
    dajax = Dajax()
    u=User.objects.get(id=user_id)
    if request.user.is_superuser:
        if u.is_staff:
            u.is_staff=False
            dajax.script('noty({"text":"<b>Rimossi</b> i privilegi di staff all\'utente <b>'+str(u)+'</b>","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});')
        else:
            u.is_staff=True
            dajax.script('noty({"text":"<b>Aggiunti</b> i privilegi di staff all\'utente <b>'+str(u)+'</b>","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});')
        u.save()
    else:
        dajax.script('noty({"text":"Solo l\'amministratore puo modificare i permessi degli utenti","layout":"bottomRight","type":"error","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});')
        if u.is_staff:
            dajax.assign('input#staff-'+str(user_id),'checked',True)
        else:
            dajax.assign('input#staff-'+str(user_id),'checked',False)
    return dajax.json()

@dajaxice_register
def notifiche(request,option,url):
    dajax = Dajax()
    #pdb.set_trace()
    i=0
    dajax.assign('#sele','value','')
    for not_id in url.rsplit('_'):
        i += 1
        selector='#not-'+not_id
        m = Notifica.objects.get(id=not_id)
        if (option == 'letto'):
            m.letto=True
            m.save()
            dajax.remove_css_class(selector,'warning')
        if (option == 'nonletto'):
            m.letto=False
            m.save()
            dajax.add_css_class(selector,'warning')
        if (option == 'cancella'):
            m.delete()
            dajax.remove(selector)
            dajax.remove('#not-inv-'+not_id)
            #dajax.alert(request.user.get_profile().nonletti())
    non=request.user.get_profile().notifiche_non_lette()
    if non >0:
    	dajax.assign('#notifiche-badge','innerHTML',non)
    else:
		dajax.assign('#notifiche-badge','innerHTML','')
    dajax.clear('.ch','checked')
    return dajax.json()


@dajaxice_register
def tipo_turno_form(request, form):
    dajax = Dajax()
    form = TipoTurnoForm(deserialize_form(form))
    if form.is_valid():
        f=form.save()
        tipo_turno=TipoTurno.objects.get(id=f.id)
        mansioni=Mansione.objects.all()
        html_dettagli = render_to_string( 'elenco_tipo_turno/dettagli.html', { 'tipo_turno': tipo_turno, 'mansioni': mansioni,'operatori': OPERATORI } )
        #dajax.alert(html_dettagli)
        dajax.append('#elenco', 'innerHTML', html_dettagli)
        dajax.script('$("#form_tipo_turno" ).dialog("close"); $( "div#tipo_turno-'+str(f.id)+'.riga a").button(); $( ".dettagli_requisito").hide();')
        #dajax.alert("aggiunto!")
    else:
        dajax.remove_css_class('#form_tipo_turno input', 'error')
        for error in form.errors:
            dajax.add_css_class('#id_%s' % error, 'ui-state-error')
    return dajax.json()

@dajaxice_register
def elimina_tipo_turno(request,turno_id):
    dajax = Dajax()
    t=TipoTurno.objects.get(id=turno_id)
    t.delete()
    return dajax.json()

@dajaxice_register
def requisito_form(request, form, form_id):
    dajax = Dajax()
    #pdb.set_trace()
    f = deserialize_form(form)
    if Requisito.objects.filter(mansione=f['mansione'],tipo_turno=f['tipo_turno']).exists():
        r = Requisito.objects.get(mansione=f['mansione'],tipo_turno=f['tipo_turno'])
        form = RequisitoForm(f,instance=r)
    else:
        form = RequisitoForm(f)
    dajax.remove_css_class(str(form_id)+ ' #id_operatore', 'ui-state-error')
    dajax.remove_css_class(str(form_id)+ ' #id_valore', 'ui-state-error')
    if form.data.get('operatore')=='NULL' and Requisito.objects.filter(mansione=f['mansione'],tipo_turno=f['tipo_turno']).exists():
        r=Requisito.objects.get(mansione=form.data.get('mansione'),tipo_turno=form.data.get('tipo_turno'))
        turni=Turno.objects.filter(tipo=form.data.get('tipo_turno'))
        for t in turni:
             for d in Disponibilita.objects.filter(turno=t, mansione=form.data.get('mansione')):
                d.mansione=None
                d.save()
        r.delete()
        dajax.script('$("#applica-'+str(form.data.get('mansione'))+'-'+str(form.data.get('tipo_turno'))+'").hide();')
        dajax.assign(str(form_id)+ ' input', 'value','')
    elif form.is_valid():
        form.save()
        dajax.script('$("#applica-'+str(form.data.get('mansione'))+'-'+str(form.data.get('tipo_turno'))+'").hide();')
	dajax.script('noty({"text":"Modifiche apportate con successo","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});')
    else:
        for error in form.errors:
            dajax.add_css_class('%(form)s #id_%(error)s' % {"form": form_id, "error": error}, 'ui-state-error')
    return dajax.json()

@dajaxice_register
def disp(request, turno_id, mansione_id, persona_id, disp):
	dajax = Dajax()
	#pdb.set_trace()
	p=Persona.objects.get(id=persona_id)
	t=Turno.objects.get(id=turno_id)
	if Disponibilita.objects.filter(persona=p,turno=t, tipo="Disponibile" ).exists():
		d=Disponibilita.objects.get(persona=p,turno=t, tipo="Disponibile" )
		dajax.remove('#disponibile-'+str(d.id))
	nuova_disponibilita(request, turno_id, mansione_id, persona_id, disp)
	d=Disponibilita.objects.get(persona=p,turno=t)
	if d.tipo=="Disponibile":
		dajax.append('#disponibili', 'innerHTML', '<span id="disponibile-'+str(d.id)+'" class="disponibile">'+str(d.persona)+' ('+str(d.mansione)+')</span>')
	#dajax.alert(disponibilita)
	dajax.script('noty({"text":"Aggiornata disponibilita per '+str(p)+'","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});')
	return dajax.json()

@dajaxice_register
def aggiorna_statistiche(request,da,al):
	dajax=Dajax()
	if (da!="" and al!=""):
		data_da=datetime.datetime.strptime(da, "%d/%m/%Y").date()
		data_al=datetime.datetime.strptime(al, "%d/%m/%Y").date()
		dati=statistiche_intervallo(request,data_da,data_al)
		html_statistiche = render_to_string( 'statistiche/statistiche.html', { 'dati': dati, 'elenco_statistiche': elenco_statistiche, 'request':request } )
		dajax.assign('div #stat', 'innerHTML', html_statistiche)
		#dajax.alert("ciao")
	return dajax.json()

@dajaxice_register
def elenco_cerca_persone(request,cerca):
	#pdb.set_trace()
	dajax=Dajax()
	persone=Persona.objects.filter(Q(nome__icontains=cerca) | Q(cognome__icontains=cerca))
	html_persona=render_to_string( 'persone/tabella_persone.html', { 'persone': persone, 'stati':STATI, 'request':request } )
	dajax.assign("div#tabella_persone", "innerHTML", html_persona)
	return dajax.json()

@dajaxice_register
def persona_stato(request,stato,persona):
	dajax=Dajax()
	per=Persona.objects.get(id=persona)
	per.stato=stato
	per.save()
	dajax.script('noty({"text":"Modifiche apportate con successo","layout":"bottomRight","type":"success","animateOpen":{"height":"toggle"},"animateClose":{"height":"toggle"},"speed":500,"timeout":5000,"closeButton":true,"closeOnSelfClick":true,"closeOnSelfOver":false});')
	return dajax.json()	
