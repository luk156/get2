# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from get2.calendario.models import *
from django.shortcuts import render_to_response, redirect, render
import calendar,datetime,locale
from django.db.models import Q, Count, Sum
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
import pdb
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import csv, codecs
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import redirect_to_login
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def export_csv(request, queryset, export_data, filter_by=None, file_name='exported_data.csv',
        object_id=None, not_available='n.a.', require_permission=None):
    '''
    Export objects from a queryset

    @param queryset: the queryset containing a list of objects
    @param export_data: a dictionary of the form 'path.to.data': 'Column Title'
    @param filter_by: filter the queryset by this column__condition and object_id
    @param file_name: the file name offered in the browser or a callable
    @param object_id: if file_name is callable and object_id is given, then the
        file_name is determined by calling file_name(object_id)
    @param not_available: the default data if a given object in export_data
        is not available
    @param require_permission: only user's havig the required permission can
        access this view

    Example usage:
    'queryset': User.objects.all(),
    'filter_by': 'is_active',
    'object_id': 1,
    'export_data':  [
        ('username', 'User name'),
        ('get_full_name', 'Full name'),
        ('get_profile.some_profile_var', 'Some data'),
        ]
    '''
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



def home(request):
	if Calendario.objects.all():
		c=Calendario.objects.all()[0]
		return redirect('/calendario/'+str(c.id)+'/oggi')
	else:
		return redirect('/impostazioni/calendario/nuovo/')

####   touch   ####

def touch(request,v):
	risposta=HttpResponseRedirect('/')
	risposta.set_cookie('touch', max_age=60*60*24*365, value=v)
	return risposta


#####   calendario   ####

def pasqua(anno):
  if anno<1583 or anno>2499: return None
  tabella={15:(22, 2), 16:(22, 2), 17:(23, 3), 18:(23, 4), 19:(24, 5),
           20:(24, 5), 21:(24, 6), 22:(25, 0), 23:(26, 1), 24:(25, 1)}
  m, n = tabella[anno//100]
  a=anno%19
  b=anno%4
  c=anno%7
  d=(19*a+m)%30
  e=(2*b+4*c+6*d+n)%7
  giorno=d+e
  if (d+e<10):
    giorno+=22
    mese=3
  else:
    giorno-=9
    mese=4
    if ((giorno==26) or ((giorno==25) and (d==28) and (e==6) and (a>10))):
      giorno-=7
  return giorno, mese

def festivo(giorno):
	feste=(
		(1,1),
		(1,6),
		(4,25),
		(5,1),
		(06,02),
		(8,15),
		(11,01),
		(12,8),
		(12,25),
		(12,26),
	)
	if (giorno.weekday() == 6) or ((giorno.month,giorno.day) in feste):
		return True
	p_g,p_m=pasqua(giorno.year)
	if (giorno.day == p_g and giorno.month == p_m):
		return True
	precedente=giorno-datetime.timedelta(days=1)
	if (precedente.day == p_g and precedente.month == p_m):
		return True
	return False

def prefestivo(giorno):
	successivo=giorno+datetime.timedelta(days=1)
	if festivo(successivo) and not festivo(giorno):
		return True
	return False

def calendario(request,cal_id):
	c=Calendario(id=cal_id)

	if 'start' in request.session:
		start=request.session['start']
	else:
		start=datetime.datetime.today()
	start=start.replace(hour=1,second=0,microsecond=0)

	form = FiltroCalendario()
	if request.method == 'POST':
		form = FiltroCalendario(request.POST)
		if form.is_valid():
			request.session['form_data'] = form.cleaned_data

	if 'form_data' in request.session:
		form = FiltroCalendario(initial=request.session.get('form_data'))
		g=request.session['form_data']['giorni']
		if len(g)==0:
			request.session.pop('form_data')

	#start=datetime.datetime(anno,mese,giorno,1)
	giorni = []
	turni = []
	i=0
	#pdb.set_trace()
	s=start
	if request.session.get('form_data'):
		while i<7:
			if (str(start.weekday()) in g) or (('101' in g) and prefestivo(start)) or (('102' in g) and festivo(start)) or ('99' in g) or (('103' in g) and (not prefestivo(start) and not festivo(start)) ):
				giorni.append(start)
				i=i+1
				stop = start + datetime.timedelta(days=1)
				turni.append(Turno.objects.filter(inizio__range=(start, stop),calendario=c).order_by('inizio', 'tipo__priorita'))
			start = start + datetime.timedelta(days=1)
		stop = start
		start = s
	else:
		while i<7:
			giorni.append(start)
			stop = start + datetime.timedelta(days=1)
			turni.append(Turno.objects.filter(inizio__range=(start, stop),calendario=c).order_by('inizio', 'tipo__priorita'))
			start = start + datetime.timedelta(days=1)
			i=i+1
		stop = start
		start = s

	touch=""
	if request.COOKIES.has_key('touch'):
		touch=request.COOKIES['touch']

	calendario = []
	calendario.append(giorni)
	calendario.append(turni)

	calendario=zip(*calendario)
	tipo_turno=TipoTurno.objects.all()
	gruppi=Gruppo.objects.all()

	corpo=render(request,'calendario.html',{'form_filtro':form, 'calendario':calendario,'cal_id':cal_id,'start':start,'request':request,'tipo_turno':tipo_turno,'gruppi':gruppi,'touch':touch})
	risposta = HttpResponse(corpo)
	request.session['start'] = start
	request.session['stop'] = stop
	risposta.set_cookie('sezione', value='calendario')
	return risposta

def calendarioazione(request,cal_id,azione):
	if azione == 'oggi':
		start = datetime.datetime.today()
	else:
		start = request.session['start']
	if azione == 'avanti':
		start += datetime.timedelta(days=1)
	if azione == 'indietro':
		start -= datetime.timedelta(days=1)
	if azione == 'settavanti':
		start += datetime.timedelta(days=7)
	if azione == 'settindietro':
		start -= datetime.timedelta(days=7)
	risposta = HttpResponseRedirect('/calendario/'+str(cal_id))
	request.session['start'] = start
	return risposta

@user_passes_test(lambda u:u.is_staff)
def cerca_persona(request, turno_id, mansione_id):
	mansione=Mansione.objects.get(id=mansione_id)
	persone=Persona.objects.filter(competenze=mansione).order_by('cognome').exclude(stato='indisponibile')
	turno=Turno.objects.get(id=turno_id)
	return render(request,'cerca_persona.html',{'persone':persone,'t':turno,'mansione':mansione,'DISPONIBILITA':DISPONIBILITA,'request':request})


####   fine calendario   ####

####   disponibilita   ####


def verifica_intervallo(turno,persona):
	now=datetime.datetime.now()
	diff=turno.inizio-now
	if diff.days<0:
		verifica=False
		errore='Turno passato'
	elif persona.persona_disponibilita.filter(turno=turno, tipo="Disponibile") and diff.days<settings.GET_CANC_MIN:
		verifica=False
		errore='Troppo vicino (intervallo minore di '+str(settings.GET_CANC_MIN)+' giorni)'
	elif persona.persona_disponibilita.filter(turno=turno, tipo="Disponibile") and diff.days<settings.GET_CANC_MAX:
		verifica=False
		errore='Troppo lontano (intervallo maggiore di '+str(settings.GET_CANC_MAX)+' giorni)'
	elif diff.days<settings.GET_DISP_MIN:
		verifica=False
		errore='Troppo vicino (intervallo minore di '+str(settings.GET_DISP_MIN)+' giorni)'
	elif diff.days>settings.GET_DISP_MAX:
		verifica=False
		errore='Troppo lontano (intervallo maggiore di '+str(settings.GET_DISP_MAX)+' giorni)'
	else:
		verifica=True
		errore=''
	return (verifica,errore)


def disponibilita_verifica_tempo(request, turno):
#	pdb.set_trace()
	if request.user.is_staff:
		verifica=True
		errore=''
	else:
		(verifica,errore)=verifica_intervallo(turno,request.user.get_profile())
	#cprint errore
	#print diff.days
	return (verifica,errore)


# attenzione ai permessi
def rimuovi_disponibilita(request, disp_id):
	d=Disponibilita.objects.get(id=disp_id)
	if request.user.is_staff or request.user.get_profile()==d.persona:
		d.tipo='Indisponibile'
		d.save()
		notifica_disponibilita(request,d.persona,d.turno,'Non piu disponibile',d.mansione)
	return HttpResponseRedirect('/calendario')

def disponibilita_risolvi_contemporaneo(request,persona_id,contemporaneo):
	if Disponibilita.objects.filter(persona_id=persona_id,turno=contemporaneo).exists():
		for d in Disponibilita.objects.filter(persona_id=persona_id,turno=contemporaneo):
			if d.tipo=="Disponibile":
				persona= Persona.objects.get(id=persona_id)
				notifica_disponibilita(request,persona,contemporaneo,'Non piu disponibile per impegno contemporaneo',d.mansione)
			rimuovi_disponibilita(request,d.id)


def nuova_disponibilita(request, turno_id, mansione_id, persona_id, disponibilita):
	#inizializzo ma non salvo un oggetto disponibilita
	#pdb.set_trace()
	per=Persona.objects.get(id=persona_id)
	if request.user.is_staff or request.user.get_profile()==per:
		disp=Disponibilita()
		disp.tipo=disponibilita
		disp.persona=per
		disp.ultima_modifica=datetime.datetime.now()
		disp.creata_da=request.user
		disp.turno=Turno.objects.get(id=turno_id)
		disp.mansione=Mansione.objects.get(id=mansione_id)
		#verifico se la disponibilita e entro i tempi corretti
		verifica_tempo=disponibilita_verifica_tempo(request, disp.turno)
		if verifica_tempo[0]:
			#una persona puo avere una sola disponibilita per turno
			if Disponibilita.objects.filter(persona=disp.persona,turno=disp.turno ).exists():
				esistente=Disponibilita.objects.get(persona=disp.persona, turno=disp.turno )
				disp.note=esistente.note
				#if esistente.tipo=='Disponibile':
					#notifica_disponibilita(request,esistente.persona,esistente.turno,'Non piu disponibile',esistente.mansione)
				esistente.delete()
			#risolvo i conflitti con i turni contemporanei
			for contemporaneo in disp.turno.contemporanei():
				if contemporaneo != disp.turno:
					disponibilita_risolvi_contemporaneo(request,persona_id,contemporaneo)
			disp.save()
			if not request.user.is_staff:
				notifica_disponibilita(request,disp.persona,disp.turno,disponibilita,disp.mansione)
		return verifica_tempo
	else:
		return (False,'non autorizzato')


def disponibilita_url(request, turno_id, mansione_id, persona_id, disponibilita):
	d=nuova_disponibilita(request, turno_id, mansione_id, persona_id, disponibilita)
	t=Turno.objects.get(id=turno_id)
	if d[0]:
		return HttpResponseRedirect('/calendario/'+str(t.calendario.id))
	else:
		print d[1]

@user_passes_test(lambda u:u.is_staff)
def disponibilita_gruppo(request,turno_id,gruppo_id):
	turno=Turno.objects.get(id=turno_id)
	gruppo=Gruppo.objects.get(id=gruppo_id)
	return render(request,'disponibilita_gruppo.html',{'t':turno,'gruppo':gruppo,'request':request})

####   fine disponibilita   ####

####   notifica   ####

def notifica_disponibilita(request,persona,turno,tipo_disponibilita,mansione):
	messaggio='%s si e reso <b> %s </b> con mansione di <b>%s</b> per il turno del<b> %s </b> delle ore<b> %s - %s </b>' % (str(persona), str(tipo_disponibilita),str(mansione), turno.inizio.strftime("%d-%m-%Y"), turno.inizio.strftime("%H:%M"), turno.fine.strftime("%H:%M"))
	now=datetime.datetime.now()
	notifica=Notifica()
	notifica.testo=messaggio
	notifica.data=now
	notifica.letto=False
	if Impostazioni_notifica.objects.filter(giorni__contains=turno.inizio.weekday(),tipo_turno=turno.tipo):
		for i in Impostazioni_notifica.objects.filter(giorni__contains=turno.inizio.weekday(),tipo_turno=turno.tipo):
			#pdb.set_trace()
			notifica.destinatario_id=i.utente.id
			notifica.save()
	else:
		notifica.destinatario_id=settings_calendario.ID_ADMIN_NOTIFICHE # se non c'e regola va al admin
		notifica.save()
	return True

@user_passes_test(lambda u:u.is_staff)
def elenco_notifica(request):
	u=request.user
	notifiche=Notifica.objects.filter(destinatario=u).order_by('data').reverse()
	return render(request,'notifiche.html',{'notifiche':notifiche,'request':request})

#un utente dello staf potrebbe cancellare delle notifiche di altri!!!

@user_passes_test(lambda u: u.is_staff)
def elimina_notifica(request,notifica_id):
	n=Notifica.objects.get(id=notifica_id)
	n.delete()
	return HttpResponseRedirect('/notifiche/')

####   fine notifica   ####

####   inizio utenti   ####
@user_passes_test(lambda u:u.is_staff)
def elenco_utente(request):
	#if request.user.is_staff:
	utenti = User.objects.all()
	persone = Persona.objects.all().order_by('cognome','nome')
	risposta = HttpResponse(render(request,'elenco_utente.html',{'utenti':utenti,'persone':persone,'request':request,}))
	return risposta
	#else:
	#	return render(request,'staff-no.html')

@user_passes_test(lambda u:u.is_staff)
def nuovo_utente(request):
	#if request.user.is_staff:
	# Do something for anonymous users.
	azione = 'nuovo';
	if request.method == 'POST': # If the form has been submitted...
		form = UserCreationForm2(request.POST) # A form bound to the POST data
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/utenti/') # Redirect after POST
	else:
		form = UserCreationForm2()
	return render(request,'form_utente.html',{'request':request, 'form': form,'azione': azione})

@user_passes_test(lambda u:u.is_staff)
def modifica_utente(request,utente_id):
	azione = 'modifica'
	user = User.objects.get(id=utente_id)
	if request.method == 'POST': # If the form has been submitted..
		form = UserChangeForm2(request.POST, instance=user,)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/utenti/') # Redirect after POST
	else:
		form = UserChangeForm2(instance=user)
	return render(request,'form_utente.html',{'request':request, 'form': form,'azione': azione, 'user': user,})

@user_passes_test(lambda u:u.is_superuser)
def elimina_utente(request,utente_id):
	user = User.objects.get(id=utente_id)
	user.delete()
	return HttpResponseRedirect('/utenti/') # Redirect after POST

@user_passes_test(lambda u:u.is_staff)
def modifica_password_utente(request,utente_id):
	user = User.objects.get(id=utente_id)
	if request.method == 'POST': # If the form has been submitted...
		form = AdminPasswordChangeForm(user=user, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/utenti/') # Redirect after POST
	else:
		form = AdminPasswordChangeForm(user=user)
	return render(request,'form_password_utente.html',{'request':request, 'form': form, 'user': user,})

def modifica_password_personale(request,utente_id):
	user = User.objects.get(id=utente_id)
	if request.user.is_staff or request.user==user:
		if request.method == 'POST': # If the form has been submitted...
			form = PasswordChangeForm(user=user, data=request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/') # Redirect after POST
		else:
			form = PasswordChangeForm(user=user)
		return render(request,'form_password_personale.html',{'request':request, 'form': form, 'user': user,})
	else:
		raise PermissionDenied

####   fine utenti   ####

#### inizio mansioni ####
@user_passes_test(lambda u: u.is_superuser)
def nuovo_mansione(request, padre_id):
	m=None
	if padre_id!='0':
		m=Mansione.objects.get(id=padre_id)
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		form = MansioneForm(request.POST) # A form bound to the POST data
		form.helper.form_action = '/impostazioni/mansione/nuovo/'+str(padre_id)+'/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni') # Redirect after POST
	else:
		form = MansioneForm(initial={'padre': m,})
		form.helper.form_action = '/impostazioni/mansione/nuovo/'+str(padre_id)+'/'
	return render(request,'form_mansione.html',{'request':request, 'form': form,'azione': azione})

@user_passes_test(lambda u: u.is_superuser)
def modifica_mansione(request, mansione_id):
	azione = 'modifica'
	mansione = Mansione.objects.get(id=mansione_id)
	if request.method == 'POST': # If the form has been submitted...
		form = MansioneForm(request.POST, instance=mansione) # necessario per modificare la riga preesistente
		form.helper.form_action = '/impostazioni/mansione/modifica/'+str(mansione.id)+'/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		form = MansioneForm(instance=mansione)
		form.helper.form_action = '/impostazioni/mansione/modifica/'+str(mansione.id)+'/'
	return render(request,'form_mansione.html',{'form':form,'azione': azione, 'mansione': mansione,'request':request})

@user_passes_test(lambda u: u.is_superuser)
def elimina_mansione(request,mansione_id):
	m=Mansione.objects.get(id=mansione_id)
	m.delete()
	return HttpResponseRedirect('/impostazioni/')

#### fine mansioni ####

#### inzio tipo turno ####


@user_passes_test(lambda u:u.is_staff)
def impostazioni(request):
	return render(request,'impostazioni.html',{
		'tipi_turno':TipoTurno.objects.all(),
		'calendari':Calendario.objects.all(),
		'tipo_turno_form':TipoTurnoForm(),
		'mansioni':Mansione.objects.filter(padre__isnull=True),
		'impostazioni_notifica_utente':Impostazioni_notifica.objects.all(),
		'request':request})

@user_passes_test(lambda u: u.is_superuser)
def nuovo_calendario(request):
	azione = 'Nuovo'
	if request.method == 'POST': # If the form has been submitted...
		form = CalendarioForm(request.POST) # A form bound to the POST data
		form.helper.form_action = '/impostazioni/calendario/nuovo/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		form = CalendarioForm()
		form.helper.form_action = '/impostazioni/calendario/nuovo/'
	return render(request,'form_calendario.html',{'form':form,'azione':azione,'request':request})

@user_passes_test(lambda u: u.is_superuser)
def modifica_calendario(request, cal_id):
	azione = 'Modifica';
	cal = Calendario.objects.get(id=cal_id)
	if request.method == 'POST': # If the form has been submitted...
		form = CalendarioForm(request.POST, instance=cal) # necessario per modificare la riga preesistente
		form.helper.form_action = '/impostazioni/calendario/modifica/'+str(cal.id)+'/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		form = CalendarioForm(instance=cal)
		form.helper.form_action = '/impostazioni/calendario/modifica/'+str(cal.id)+'/'
	return render(request,'form_tipo_turno.html',{'form': form,'azione': azione, 'request':request})

@user_passes_test(lambda u: u.is_superuser)
def elimina_calendario(request,cal_id):
	c=Calendario.objects.get(id=cal_id)
	c.delete()
	return HttpResponseRedirect('/impostazioni/')


@user_passes_test(lambda u: u.is_superuser)
def nuovo_tipo_turno(request):
	azione = 'Nuovo'
	if request.method == 'POST': # If the form has been submitted...
		form = TipoTurnoForm(request.POST) # A form bound to the POST data
		form.helper.form_action = '/impostazioni/tipo_turno/nuovo/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		form = TipoTurnoForm()
		form.helper.form_action = '/impostazioni/tipo_turno/nuovo/'
	return render(request,'form_tipo_turno.html',{'form':form,'azione':azione,'request':request})

@user_passes_test(lambda u: u.is_superuser)
def modifica_tipo_turno(request, tipo_turno_id):
	azione = 'Modifica';
	tipo_turno = TipoTurno.objects.get(id=tipo_turno_id)
	if request.method == 'POST': # If the form has been submitted...
		form = TipoTurnoForm(request.POST, instance=tipo_turno) # necessario per modificare la riga preesistente
		form.helper.form_action = '/impostazioni/tipo_turno/modifica/'+str(tipo_turno.id)+'/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		form = TipoTurnoForm(instance=tipo_turno)
		form.helper.form_action = '/impostazioni/tipo_turno/modifica/'+str(tipo_turno.id)+'/'
	return render(request,'form_tipo_turno.html',{'form': form,'azione': azione, 'tipo_turno': tipo_turno,'request':request})

@user_passes_test(lambda u: u.is_superuser)
def elimina_tipo_turno(request,tipo_turno_id):
	t=TipoTurno.objects.get(id=tipo_turno_id)
	t.delete()
	return HttpResponseRedirect('/impostazioni/')

@user_passes_test(lambda u: u.is_staff)
def nuovo_impostazioni_notifica(request):
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		impostazioni_notifica_form = Impostazioni_notificaForm(request.POST) # A form bound to the POST data
		impostazioni_notifica_form.helper.form_action = '/impostazioni/notifica/nuovo/'
		if impostazioni_notifica_form.is_valid():
			impostazioni_notifica_form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-notifiche') # Redirect after POST
	else:
		impostazioni_notifica_form = Impostazioni_notificaForm()
		impostazioni_notifica_form.helper.form_action = '/impostazioni/notifica/nuovo/'
	return render(request,'form_impostazioni_statistiche.html',{'form':impostazioni_notifica_form,'azione':azione,'request':request})

@user_passes_test(lambda u: u.is_staff)
def modifica_impostazioni_notifica(request, impostazioni_notifica_id):
	azione = 'modifica';
	impostazioni_notifica = Impostazioni_notifica.objects.get(id=impostazioni_notifica_id)
	if request.method == 'POST': # If the form has been submitted...
		impostazioni_notifica_form = Impostazioni_notificaForm(request.POST, instance=impostazioni_notifica)
		impostazioni_notifica_form.helper.form_action = '/impostazioni/notifica/modifica/'+str(impostazioni_notifica.id)+'/'
		if impostazioni_notifica_form.is_valid():
			impostazioni_notifica_form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-notifiche') # Redirect after POST
	else:
		impostazioni_notifica_form = Impostazioni_notificaForm(instance=impostazioni_notifica)
		impostazioni_notifica_form.helper.form_action = '/impostazioni/notifica/modifica/'+str(impostazioni_notifica.id)+'/'
	return render(request,'form_impostazioni_statistiche.html',{'form': impostazioni_notifica_form,'azione': azione, 'impostazioni_notifica': impostazioni_notifica,'request':request})

@user_passes_test(lambda u: u.is_staff)
def elimina_impostazioni_notifica(request, impostazioni_notifica_id):
	i=Impostazioni_notifica.objects.get(id=impostazioni_notifica_id)
	i.delete()
	return HttpResponseRedirect('/impostazioni/#tabs-notifiche')

#### fine tipo turno ####

#### inizio turno ####
@user_passes_test(lambda u:u.is_staff)
def nuovo_turno(request, cal_id):
	#request.set_trace()
	azione = 'Aggiungi'
	if request.method == 'POST': # If the form has been submitted...
		form = TurnoFormRipeti(request.POST) # A form bound to the POST data
		form.helper.form_action = '/turno/'+str(cal_id)+'/nuovo/'
		if form.is_valid():
			data = form.cleaned_data
			if not data.get('ripeti'):
				form.save()
			else:
				o=Occorrenza()
				o.save()
				start=data.get('ripeti_da')
				stop=data.get('ripeti_al')
				giorno=data.get('ripeti_il_giorno')
				ora_inizio=data.get('inizio').time()
				start=datetime.datetime.combine(start,ora_inizio)
				durata=data.get('fine')-data.get('inizio')
				delta = datetime.timedelta(days=1)
				data['tipo']=data['tipo'].id
				data['occorrenza']=o.id
				data['calendario']=data['calendario'].id
				#pdb.set_trace()
				while (start.date()<=stop):
					data['inizio']=start
					data['fine']=(start+durata)
					f=TurnoFormRipeti(data)
					if ((str(start.weekday()) in giorno) or (('101' in giorno) and prefestivo(start)) or (('102' in giorno) and festivo(start)) or ('99' in giorno) or (('103' in giorno) and (not prefestivo(start) and not festivo(start)) )) and f.is_valid():
						t=f.save()
						t.occorrenza=o
						t.save()
					start+=delta
			return HttpResponseRedirect('/calendario/'+str(cal_id)) # Redirect after POST
	else:
		c=Calendario.objects.get(id=cal_id)
		form = TurnoFormRipeti(initial={'calendario': c, 'coperto': False })
		form.helper.form_action = '/turno/'+str(cal_id)+'/nuovo/'
	return render(request,'form_turno.html',{'form': form,'azione': azione,'request':request})

@user_passes_test(lambda u:u.is_staff)
def modifica_turno(request, turno_id):
	azione = 'Modifica';
	turno = Turno.objects.get(id=turno_id)
	if request.method == 'POST': # If the form has been submitted...
		form = TurnoForm(request.POST, instance=turno) # necessario per modificare la riga preesistente
		form.helper.form_action = '/turno/modifica/'+str(turno.id)+'/'
		if form.is_valid():
			data = form.cleaned_data
			form.save()
			#pdb.set_trace()
			occ=False
			if 'modifica_tutti' in request.POST:
				occorrenze = Turno.objects.filter(occorrenza=turno.occorrenza)
				occ=True
			elif 'modifica_futuri' in request.POST:
				occorrenze = Turno.objects.filter(occorrenza=turno.occorrenza, inizio__gte=turno.inizio)
				occ=True
			if occ:
				for o in occorrenze:
					o.tipo=turno.tipo
					o.valore=turno.valore
					o.identificativo=turno.identificativo
					o.calendario=turno.calendario
					i=o.inizio.replace(hour=turno.inizio.hour, minute=turno.inizio.minute)
					f=o.fine.replace(hour=turno.fine.hour, minute=turno.fine.minute)
					o.inizio=i
					o.fine=f
					o.save()
			return HttpResponseRedirect('/calendario/'+str(turno.calendario.id)) # Redirect after POST
	else:
		form = TurnoForm(instance=turno)
		form.helper.form_action = '/turno/modifica/'+str(turno.id)+'/'
		if turno.occorrenza:
			form.helper.layout[4].append(Fieldset("Il turno fa parte di una occorrenza","modifica_futuri"))
			if request.user.is_superuser:
				form.helper.layout[4][1].append("modifica_tutti")
	return render(request,'form_turno.html',{'form': form,'azione': azione, 'turno': turno,'request':request})

@user_passes_test(lambda u:u.is_staff)
def elimina_turno(request, turno_id):
	t = Turno.objects.get(id=turno_id)
	cal_id=t.calendario.id
	t.delete()
	return HttpResponseRedirect('/calendario/'+str(cal_id))

@user_passes_test(lambda u:u.is_staff)
def elimina_turno_occorrenza_succ(request, occorrenza_id):
	o=Occorrenza.objects.get(id=occorrenza_id)
	turni = Turno.objects.filter(occorrenza=o, inizio__gte=datetime.datetime.now())
	cal_id=turni[0].calendario.id
	for t in turni:
		t.delete()
	return HttpResponseRedirect('/calendario/'+str(cal_id))

@user_passes_test(lambda u: u.is_superuser)
def elimina_turno_occorrenza(request, occorrenza_id):
	o=Occorrenza.objects.get(id=occorrenza_id)
	turni = Turno.objects.filter(occorrenza=o)
	cal_id=turni[0].calendario.id
	for t in turni:
		t.delete()
	return HttpResponseRedirect('/calendario/'+str(cal_id))

#### fine turno ####


#### inizio requisito ####
@user_passes_test(lambda u: u.is_superuser)
def nuovo_requisito(request,tipo_turno_id):
	t_turno=TipoTurno(id=tipo_turno_id)
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		form = RequisitoForm(request.POST) # A form bound to the POST data
		form.helper.form_action = '/impostazioni/tipo_turno/aggiungi_requisito/'+str(t_turno.id)+'/'
		if form.is_valid():
			r=Requisito(tipo_turno=t_turno)
			form =  RequisitoForm(request.POST, instance=r)
			form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-tipo-turno') # Redirect after POST
	else:
		form = RequisitoForm(initial={'necessario': True,})
		form.helper.form_action = '/impostazioni/tipo_turno/aggiungi_requisito/'+str(t_turno.id)+'/'
	return render(request,'form_requisito.html',{'request':request, 'tipo_turno': t_turno, 'form': form,'azione': azione})

@user_passes_test(lambda u: u.is_superuser)
def modifica_requisito(request,requisito_id):
	azione = 'modifica'
	requisito = Requisito.objects.get(id=requisito_id)
	if request.method == 'POST': # If the form has been submitted...
		form = RequisitoForm(request.POST, instance=requisito) # necessario per modificare la riga preesistente
		form.helper.form_action = '/impostazioni/requisito/modifica/'+str(requisito.id)+'/'
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/#tabs-tipo-turno') # Redirect after POST
	else:
		form = RequisitoForm(instance=requisito)
		form.helper.form_action = '/impostazioni/requisito/modifica/'+str(requisito.id)+'/'
	return render(request,'form_requisito.html',{'form':form,'azione': azione,'requisito': requisito,'request':request})

@user_passes_test(lambda u: u.is_superuser)
def elimina_requisito(request,requisito_id):
	m=Requisito.objects.get(id=requisito_id)
	m.delete()
	return HttpResponseRedirect('/impostazioni/#tabs-tipo-turno')

#### fine requisito ####

