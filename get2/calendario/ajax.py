#from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from get2.calendario.models import *
from get2.calendario.views import *
from dajaxice.utils import deserialize_form
import pdb
from django.template.loader import render_to_string
from django.template import Context, Template
from django.utils import simplejson
from django.conf import settings

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
    dajax.script("$('#loading').addClass('hidden');")
    return dajax.json()



@dajaxice_register
def elimina_utente(request,utente_id):
	user=User.objects.get(id=utente_id)
	dajax = Dajax()
	if request.user.is_staff:
		if (not user.is_staff or request.user.is_superuser):
			user.delete()
			dajax.remove('#utente-'+str(utente_id))
		else:
			dajax.script('$(".bottom-right").notify({ message: { text: "Solo l\'amministratore puo\' eliminare questo utente" }}).show();')
	else:
		dajax.script('$(".bottom-right").notify({ message: { text: "Solo un membro dello staff puo\' eliminare un utente" }}).show();')      
	dajax.script("$('#loading').addClass('hidden');")
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
            s=s+'$(".bottom-right").notify({ message: { text: "l\' utente '+str(a)+' non e piu assegnato a nessuna persona" }}).show();'
            pass
    if persona_id!='n' and User.objects.filter(pers_user=persona_id):
        a=User.objects.get(pers_user=persona_id)
        dajax.assign('select#select-'+str(a.id),'selectedIndex','0')
        s=s+'$(".bottom-right").notify({ message: { text: "Attenzione:La persona era precedentemente assegnato all\'utente '+str(a)+'" }}).show();'
    if persona_id!='n':
        per=Persona.objects.get(id=persona_id)
        u=User.objects.get(id=user_id)
        per.user=u
        s=s+'$(".bottom-right").notify({ message: { text: "La persona '+str(per)+' e stato assegnata all\'utente '+str(u)+'" }}).show();'
    dajax.script(s)
    per.save()
    dajax.script("$('#loading').addClass('hidden');")
    return dajax.json()

@dajaxice_register
def utente_staff(request,user_id):
    dajax = Dajax()
    u=User.objects.get(id=user_id)
    if request.user.is_superuser:
        if u.is_staff:
            u.is_staff=False
            dajax.script('$(".bottom-right").notify({ message: { text: "Rimossi i privilegi di staff all\'utente '+str(u)+'" }}).show();')
        else:
            u.is_staff=True
            dajax.script('$(".bottom-right").notify({ message: { text: "Aggiunti i privilegi di staff all\'utente '+str(u)+'" }}).show();')
        u.save()
    else:
        dajax.script('$(".bottom-right").notify({ message: { text: "Solo l\'amministratore puo modificare i permessi degli utenti" }}).show();')
        if u.is_staff:
            dajax.assign('input#staff-'+str(user_id),'checked',True)
        else:
            dajax.assign('input#staff-'+str(user_id),'checked',False)
    dajax.script("$('#loading').addClass('hidden');")
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
    try:
        non=request.user.pers_user.notifiche_non_lette()
        if non >0:
           dajax.assign('#notifiche-badge','innerHTML',non)
        else:
           dajax.assign('#notifiche-badge','innerHTML','')
    except:
        pass
    dajax.clear('.ch','checked')
    dajax.script("$('#loading').addClass('hidden');")
    return dajax.json()


@dajaxice_register
def tipo_turno_form(request, form):
    dajax = Dajax()
    form = TipoTurnoForm(deserialize_form(form))
    if form.is_valid():
        f=form.save()
        tipo_turno=TipoTurno.objects.get(id=f.id)
        mansioni=Mansione.objectsGet.all()
        html_dettagli = render_to_string( 'elenco_tipo_turno/dettagli.html', { 'tipo_turno': tipo_turno, 'mansioni': mansioni } )
        dajax.append('#elenco', 'innerHTML', html_dettagli)
        dajax.script('$("#form_tipo_turno" ).dialog("close"); $( "div#tipo_turno-'+str(f.id)+'.riga a").button(); $( ".dettagli_requisito").hide();')
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
    dajax.script("$('#loading').addClass('hidden');")
    return dajax.json()


@dajaxice_register
def disp(request, turno_id, mansione_id, persona_id, disp):
	dajax = Dajax()
	p=Persona.objects.get(id=persona_id)
	t=Turno.objects.get(id=turno_id)
	if disp!="-":
		d=nuova_disponibilita(request, turno_id, mansione_id, persona_id, disp)
		if not d[0]:
			dajax.script('$(".bottom-right").notify({ message: { text: "Errore'+str(d[1])+'" }}).show();')
		d=Disponibilita.objects.get(persona=p,turno=t)

	elif request.user.is_staff:
		d=Disponibilita.objects.get(persona=p,turno=t)
		if request.user.is_superuser or request.user==d.creata_da:
			d.delete()
			d={}
	temp = Template('<div class="input-prepend input-append small span4"><span class="add-on"><i class="icon-comment"></i></span><input id="note-disp-{{d.id}}" type="text" value="{{d.note}}"><button class="btn" type="button" onclick="nota_disponibilita({{d.id}});">salva</button></div>'
            +'{% if get_sovrascrivi_punteggio %}<div class="input-prepend input-append small span3"><span class="add-on"><i class="icon-trophy"></i></span><input id="punteggio-disp-{{d.id}}" type="number" {% if d.punteggio != -1 %} value="{{d.punteggio}}" {% else %} placeholder="{{t.valore}}" {% endif %}> <button class="btn" type="button" onclick="punteggio_disponibilita({{d.id}});">salva</button> </div>{% endif %}'
            +'</br>{{d.creata_da}}:{{d.ultima_modifica|date:"d M"}} {{d.ultima_modifica|time:"H:i"}}')
	c = Context({"d": d, "t":t, "get_sovrascrivi_punteggio": getattr(settings, 'GET_SOVRASCRIVI_PUNTEGGIO', False)})
	dajax.assign('#disponibilita-'+str(p.id), 'innerHTML', temp.render(c))
	t=Turno.objects.get(id=turno_id)
	html_anteprima = render_to_string( 'turno.html', { 't': t, 'request':request } )
	dajax.assign('div #anteprima', 'innerHTML', html_anteprima+'<div style="clear:both;"></div>')
	dajax.script('$(".bottom-right").notify({ message: { text: "Aggiornata disponibilita per '+str(p)+'" }}).show();')
	dajax.script('$(".h6-mansione-'+mansione_id+'").addClass("mansione-sel");')
	dajax.script("$('#loading').addClass('hidden');")
	return dajax.json()

@dajaxice_register
def disp_nota(request,disp_id,nota):
	dajax = Dajax()
	d=Disponibilita.objects.get(id=disp_id)
	d.note=str(nota)
	d.save()
	t=d.turno
	html_anteprima = render_to_string( 'turno.html', { 't': t, 'request':request } )
	dajax.assign('div #anteprima', 'innerHTML', html_anteprima+'<div style="clear:both;"></div>')
	dajax.script('$(".bottom-right").notify({ message: { text: "Nota modificata" }}).show();')
	return dajax.json()

@dajaxice_register
def disp_punteggio(request,disp_id,punteggio):
	dajax = Dajax()
	d=Disponibilita.objects.get(id=disp_id)
	if punteggio.isdigit():
		d.punteggio=int(punteggio)
	else:
		d.punteggio=-1
	d.save()
	dajax.script('$(".bottom-right").notify({ message: { text: "Punteggio modificato" }}).show();')
	return dajax.json()


@dajaxice_register
def occorrenze(request,occ_id,turno_id):
	dajax=Dajax()
	html=''
	for t in Turno.objects.filter(occorrenza_id=occ_id):
		html+='<li>'+str(t.inizio)+'</li>'
	dajax.assign("div#occorrenze-"+str(turno_id), "innerHTML", html)
	dajax.script('$("div#occorrenze-'+str(turno_id)+'").slideDown();')
	return dajax.json()	

@dajaxice_register
def mansioni_disponibili(request,turno_id):
	dajax=Dajax()
	html=''
	t=Turno.objects.get(id=turno_id)
	mansioni = []
	for requisito in t.tipo.req_tipo_turno.all():
		if requisito.mansione in request.user.get_profile().capacita and requisito.clickabile():
			if not requisito.mansione in t.mansioni_indisponibili(request.user.get_profile().id):
				mansioni.append(requisito.mansione)
	html_disp = render_to_string( 'disponibilita_turno.html', { 't': t, 'mansioni': mansioni, 'request':request } )
	dajax.assign("#disponibilita-turno-"+str(t.id)+" > .modal-body ", "innerHTML", html_disp)
	return dajax.json()

@dajaxice_register
def elimina_turno(request,turno_id):
	dajax=Dajax()
	t=Turno.objects.get(id=turno_id)
	html_elimina = render_to_string( 'elimina_turno.html', { 't': t, 'request':request } )
	dajax.assign('div #elimina-turno-'+str(t.id), 'innerHTML', html_elimina)
	dajax.script("$('#elimina-turno-"+str(t.id)+"').modal('show');")
	return dajax.json()

@dajaxice_register
def modal_elimina_utente(request,utente_id):
	dajax=Dajax()
	u=User.objects.get(id=utente_id)
	html_elimina = render_to_string( 'elimina_utente.html', { 'utente': u, 'request':request } )
	dajax.assign('div #elimina-utente-'+str(u.id), 'innerHTML', html_elimina)
	dajax.script("$('#elimina-utente-"+str(u.id)+"').modal('show');")
	return dajax.json()

@dajaxice_register
def auto_utente_persona_search(request,search_term):
	# Query DB for suggestions to present to user
	q = Persona.objectsGet.filter(cognome__istartswith=search_term)
	data = []
	#pdb.set_trace()
	for item in q:
		# Format returned queryset data, if needed
		#data_item = str(item)
		data.append({'label': str(item), 'value': item.id})

	# Return data to callback function *search_result*
	return simplejson.dumps(data)

@dajaxice_register
def scorri_calendario(request,direction):
	dajax=Dajax()

	if direction == '+1':
		remove_day = request.session['start']
		start = request.session['start'] + datetime.timedelta(days=7)
		stop = start + datetime.timedelta(days=1)
		request.session['start'] = request.session['start'] + datetime.timedelta(days=1)

	elif direction == '-1':
		remove_day = request.session['start'] + datetime.timedelta(days=6)
		start = request.session['start']  - datetime.timedelta(days=1)
		stop = request.session['start']
		request.session['start'] = request.session['start'] - datetime.timedelta(days=1)

	c = Calendario.objects.get(id=request.session['calId'])
	t = Turno.objects.filter(inizio__range=(start, stop),calendario=c).order_by('inizio', 'tipo__priorita')
	html_giorno = render_to_string( 'giorno.html', { 'turno': t, 'giorno': start, 'request':request } )
	dajax.remove('div #giorno-'+remove_day.strftime("%d_%m_%Y"))
	if direction == '+1':
		dajax.script("$('.row-fluid.calendario').append('<div id=\"giorno-"+start.strftime("%d_%m_%Y")+"\" class=\"giorno span1\" ></div>');")
	elif direction == '-1':
		dajax.script("$('.row-fluid.calendario').prepend('<div id=\"giorno-"+start.strftime("%d_%m_%Y")+"\" class=\"giorno span1\" ></div>');")

	dajax.assign('div #giorno-'+start.strftime("%d_%m_%Y"), 'innerHTML', html_giorno)
	dajax.script("$('#loading').addClass('hidden');")
	dajax.script("window.allinea_calendario();")
	return dajax.json()
