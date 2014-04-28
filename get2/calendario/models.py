from django.db import models
from django import forms
from django.contrib.auth.models import User
import operator, datetime
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import pdb
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML
from crispy_forms.bootstrap import *
from django.utils.text import capfirst
from persone.models import *
from django.utils.functional import cached_property

class GetModelManager(models.Manager):
    def get_query_set(self):
        return super(GetModelManager, self).get_query_set().filter(cancellata=False)


STATI=(('disponibile','Disponibile'),('ferie','In ferie'),('malattia','In malattia'),('indisponibile','Indisponibile'))

GIORNI=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'))

class Calendario(models.Model):
	nome = models.CharField('Nome',max_length=20)
	priorita = models.IntegerField('priorita', default=0, )
	class Meta:
		ordering = ['priorita']
	def __unicode__(self):
		return '%s' % (self.nome)
		
class CalendarioForm(forms.ModelForm):
	class Meta:
		model = Calendario
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('nome'),
			Field('priorita'),
			FormActions(
				Submit('save', 'Invia', css_class="btn-primary")
			)
		)
		super(CalendarioForm, self).__init__(*args, **kwargs)



class TipoTurno(models.Model):
	identificativo = models.CharField(max_length=30, blank=False)
	priorita = models.IntegerField('priorita', default=0, )
	msg_errore = models.TextField('Messaggio errore disponibilita', blank=True, null=True, help_text="Il messaggio viene visualizzato nel caso non sia possibile modificare la disponibilta")
	#msg_lontano = models.TextField( blank=True, null=True, )
	cancellata =  models.BooleanField(default=False )
	objects = models.Manager()
	objectsGet = GetModelManager()
	def __unicode__(self):
		return '%s' % (self.identificativo)

class TipoTurnoForm(forms.ModelForm):
	class Meta:
		model = TipoTurno
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('identificativo'),
			Field('priorita'),
			Field('msg_errore'),
			FormActions(
				Submit('save', 'Invia', css_class="btn-primary")
			)
		)
		super(TipoTurnoForm, self).__init__(*args, **kwargs)



class Requisito(models.Model):
	mansione=models.ForeignKey(Mansione, related_name="req_mansione")
	minimo=models.IntegerField('Minimo', default=0,)
	massimo=models.IntegerField('Massimo', default=0, help_text="Se 0 non c'e' limite")
	tipo_turno=models.ForeignKey(TipoTurno, related_name="req_tipo_turno",)
	necessario=models.BooleanField('Necessario', default=True, help_text="Se selezionato il requisito deve essere soddisfatto")
	sufficiente=models.BooleanField('Sufficiente', default=False, help_text="Se il requisito e' soddisfatto il turno risulta coperto in ogni caso")
	nascosto=models.BooleanField('Nascosto', default=False, help_text="Se il requisito risulta nascosto verra comunque verificato ma la persona non potra' segnarsi in quel ruolo")
	extra=models.BooleanField('Extra', default=False, help_text="Il requisito viene verificato su tutte le capacita delle persone disponibili, indipendentemtne dal loro ruolo nel turno")
	ignora_gerarchie=models.BooleanField('Ignora gerarchie', default=False, help_text="Durante la verfica vengono ignorate le gerarchie tra le mansioni")
	def clickabile(self):
		return  not (self.extra or self.nascosto)
	def save(self, *args, **kwargs):
		super(Requisito, self).save(*args, **kwargs)
		for t in Turno.objects.filter(tipo=self.tipo_turno, inizio__gte=datetime.datetime.now().date()):
			t.coperto = t.calcola_coperto_cache
			t.save()
	def delete(self, *args, **kwargs):
		super(Requisito, self).delete(*args, **kwargs)
		for t in Turno.objects.filter(tipo=self.tipo_turno, inizio__gte=datetime.datetime.now().date()):
			t.coperto = t.calcola_coperto_cache
			t.save()

class RequisitoForm(forms.ModelForm):

	class Meta:
		model = Requisito
		exclude = ('tipo_turno',)
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('mansione'),
			Field('minimo'),
			Field('massimo'),
			Field('necessario'),
			Field('sufficiente'),
			Field('nascosto'),
			Field('extra'),
			Field('ignora_gerarchie'),
			FormActions(
				Submit('save', 'Invia', css_class="btn-primary")
			)
		)
		super(RequisitoForm, self).__init__(*args, **kwargs)
		
GIORNO = (
  (0, 'lunedi'),
  (1, 'martedi'),
  (2, 'mercoledi'),
  (3, 'giovedi'),
  (4, 'venerdi'),
  (5, 'sabato'),
  (6, 'domenica'),
  )

GIORNO_EXT = GIORNO + (
  (103, 'feriale'),
  (101, 'prefestivo'),
  (102, 'festivo'),
  (99, 'qualsiasi'),
  )

class FiltroCalendario(forms.Form):
	giorni = forms.MultipleChoiceField( label = "",	choices = GIORNO_EXT[0:10], required = False, )
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_id = 'FiltroCalendario'
		self.helper.layout = Layout(
			InlineCheckboxes('giorni'),
			ButtonHolder( Submit('submit', 'Filtra', css_class='button white'), ),)
		self.helper.form_method = 'post'
		#self.helper.form_action = 'submit_survey'
		super(FiltroCalendario, self).__init__(*args, **kwargs)

class Occorrenza(models.Model):
	pass

class Turno(models.Model):
	identificativo = models.CharField(max_length=30, blank=True , default='')
	inizio = models.DateTimeField()
	fine = models.DateTimeField()
	tipo = models.ForeignKey(TipoTurno, related_name='tipo_turno_turno', blank=True, null=True, on_delete=models.SET_NULL)
	occorrenza = models.ForeignKey(Occorrenza, blank=True, null=True)
	valore = models.IntegerField('Punteggio',default=1)
	calendario = models.ForeignKey(Calendario, related_name='calendario_turno' ,null=True, on_delete=models.SET_NULL, default=1)
	coperto = models.BooleanField(default=False)
	requisiti = models.ManyToManyField(Requisito, blank=True, null=True, related_name='requisiti_turno', through='Cache_requisito')
	def verifica_requisito(self,requisito,mansione_id=0,persona_capacita=0):
		if requisito.necessario:
			contatore=0
			if mansione_id!=0 and persona_capacita!=0:
				f=[Mansione.objects.get(id=mansione_id)]
				if not requisito.ignora_gerarchie:
					f+=figli(mansione_id)
				if (not requisito.extra and requisito.mansione in f):
					contatore+=1
				if (requisito.extra and requisito.mansione in persona_capacita):
					contatore+=1
			for d in self.turno_disponibilita.filter(tipo="Disponibile").exclude(mansione__isnull=True).all():
				if not requisito.extra:
					f=[d.mansione]
					if not requisito.ignora_gerarchie:
						f+=figli(d.mansione.id)
					if (requisito.mansione in f):
						contatore+=1
				else:
				 	if (requisito.mansione in d.persona.capacita ):
						contatore+=1
				if contatore>requisito.massimo and requisito.massimo!=0:
					return False
			if contatore<requisito.minimo and requisito.minimo!=0:
				return False
			return True
		else:
			return True
	def posti_liberi(self,requisito):
		posti = requisito.requisito.minimo - requisito.disponibilita.filter(tipo="Disponibile").exclude(mansione__isnull=True).count()
		if posti > 0:
			return range(posti)
		return range(0)
	@cached_property
	def calcola_coperto(self):
		if self.tipo:
			for r in Requisito.objects.filter(tipo_turno=self.tipo_id):
				if not self.verifica_requisito(r):
					return False
				elif r.sufficiente:
					return True
		return True
	@cached_property
	def calcola_coperto_cache(self):
		if self.tipo:
			#if not Cache_requisito.objects.filter(turno=self).filter( ( models.Q(requisito__sufficiente=True) & models.Q(verificato=True) ) | ( ~models.Q(verificato=False) ) ).count() > 0:
			#	return False
			for c in Cache_requisito.objects.filter(turno=self):
				if not c.verificato:
					return False
				elif c.requisito.sufficiente:
					return True
		return True
	@cached_property
	def contemporanei(self):
		i=self.inizio+datetime.timedelta(seconds=60)
		f=self.fine-datetime.timedelta(seconds=60)
		return Turno.objects.filter( (models.Q(inizio__lte=i) & models.Q(fine__gte=f)) | models.Q(inizio__range=(i ,f)) | models.Q(fine__range=(i,f)) ).exclude(id=self.id)
	@cached_property
	def mansioni(self):
		return Mansione.objects.filter(req_mansione__tipo_turno=self.tipo)
	def mansioni_indisponibili(self,persona):
		m_d = []
		p = Persona.objects.get(id=persona)
		persona_capacita = p.capacita
		req = self.tipo.req_tipo_turno.all()
		for m in persona_capacita:
			for r in req:
				if (self.verifica_requisito(r) and not self.verifica_requisito(r,mansione_id=m.id,persona_capacita=persona_capacita) ):
					m_d.append(m)
		return m_d
	def save(self, *args, **kwargs):
		self.inizio = self.inizio.replace(second=0)
		self.fine = self.fine.replace(second=0)
		super(Turno, self).save(*args, **kwargs)
		requisiti = self.tipo.req_tipo_turno.all()
		for c in Cache_requisito.objects.filter(turno=self):
			if c.requisito not in requisiti:
				c.delete()
		for r in requisiti:
			try:
				cr=Cache_requisito.objects.get(turno=self,requisito=r)
			except:
				cr=Cache_requisito(turno=self,requisito=r,verificato=False)
				cr.save()
			cr.verificato=self.verifica_requisito(r)
			cr.disponibilita=self.turno_disponibilita.filter(tipo="Disponibile",mansione=r.mansione)
			cr.save()
		self.coperto = self.calcola_coperto_cache
		super(Turno, self).save(*args, **kwargs)




class TurnoForm(forms.ModelForm):
	modifica_futuri=forms.BooleanField(label="modifica occorrenze future",required=False, help_text="<i class='icon-warning-sign'></i> sara' modificato solo l'orario e non la data!")
	modifica_tutti=forms.BooleanField(label="modifica tutte le occorrenze",required=False, help_text="<i class='icon-warning-sign'></i> sara' modificato solo l'orario e non la data!")
	#durata=forms.SelectField(label="Durata del turno", required=True, choices=DURATA)
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('identificativo'),
			AppendedText(
				'inizio', '<i class="icon-calendar"></i>'
			),
			AppendedText(
				'fine', '<i class="icon-calendar"></i>'
			),
			#Field('durata'),
			Field('tipo'),
			Field('valore'),
			Field('calendario'),
			FormActions(
				Submit('save', 'Modifica', css_class="btn-primary")
			)
		)
		super(TurnoForm, self).__init__(*args, **kwargs)
		self.fields['tipo'].required = True
		self.fields['tipo'].queryset = TipoTurno.objectsGet.all()
	class Meta:
		model = Turno
		exclude = ('occorrenza','requisiti')
	def clean(self):
		data = self.cleaned_data
		if data.get('inizio')>data.get('fine'):
			raise forms.ValidationError('Il turno termina prima di iniziare! controlla inizio e fine')
		if (data.get('fine')-data.get('inizio')).days>0:
			raise forms.ValidationError('Il turno deve durare al massimo 24H')
		return data
		
class TurnoFormRipeti(TurnoForm):
	ripeti = forms.BooleanField(required=False)
	ripeti_da = forms.DateField(required=False)
	ripeti_al = forms.DateField(required=False)
	ripeti_il_giorno = forms.MultipleChoiceField(choices=GIORNO_EXT, widget=forms.CheckboxSelectMultiple(),required=False)
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('identificativo'),
			AppendedText(
				'inizio', '<i class="icon-calendar"></i>'
			),
			AppendedText(
				'fine', '<i class="icon-calendar"></i>'
			),
			Field('tipo'),
			Field('valore'),
			Field('calendario'),
			Fieldset(
				'<span id="ripeti-switch" onclick="ripeti_toggle()"><i class="icon-chevron-down"></i> Ripeti turno</span>'
			),
			Div(
				Field('ripeti'),
				AppendedText(
					'ripeti_da', '<i class="icon-calendar"></i>'
				),
				AppendedText(
					'ripeti_al', '<i class="icon-calendar"></i>'
				),
				InlineCheckboxes('ripeti_il_giorno'), css_id="ripeti"
			),
			FormActions(
				Submit('save', 'Aggiungi', css_class="btn-primary")
			)
		)
		super(TurnoForm, self).__init__(*args, **kwargs)
		self.fields['tipo'].required = True
		self.fields['tipo'].queryset = TipoTurno.objectsGet.all()
	def clean(self):
		data = self.cleaned_data
		ripeti=data.get('ripeti')
		da=data.get('ripeti_da')
		al=data.get('ripeti_al')
		if (data.get('fine')-data.get('inizio')).days>0:
			raise forms.ValidationError('Il turno deve durare al massimo 24H')
		if data.get('inizio')>data.get('fine'):
			raise forms.ValidationError('Il turno termina prima di iniziare! controlla inizio e fine')
		if ripeti and (da==None or al==None):
			raise forms.ValidationError('Specifica l\' intervallo in cui ripetere il turno')
		return data



DISPONIBILITA = (("Disponibile","Disponibile"),("Indisponibile","Indisponibile"),("Darichiamare","Da Richiamare"),("Nonrisponde","Non Risponde"),)

class Disponibilita(models.Model):
	tipo = models.CharField(max_length=20, choices=DISPONIBILITA)
	persona = models.ForeignKey(Persona, related_name='persona_disponibilita', on_delete=models.PROTECT)
	ultima_modifica = models.DateTimeField()
	creata_da = models.ForeignKey(User, related_name='creata_da_disponibilita', blank=True, null=True, on_delete=models.SET_NULL)
	turno = models.ForeignKey(Turno, related_name='turno_disponibilita')
	mansione = models.ForeignKey(Mansione, related_name='mansione_disponibilita', null=True, blank=True, on_delete=models.PROTECT)
	note =  models.TextField( blank=True, null=True, default="")
	class Meta:
		ordering = ['mansione']
		unique_together = ('persona', 'turno')
	def save(self, *args, **kwargs):
		super(Disponibilita, self).save(*args, **kwargs)
		self.turno.save()
	def delete(self, *args, **kwargs):
		super(Disponibilita, self).delete(*args, **kwargs)
		self.turno.save()

class Cache_requisito(models.Model):
    turno = models.ForeignKey(Turno)
    requisito = models.ForeignKey(Requisito)
    verificato = models.BooleanField(default=False)
    disponibilita = models.ManyToManyField(Disponibilita, blank=True, null=True, related_name='disponibilita_requisito')
    class Meta:
    	ordering = ['requisito']

class Notifica(models.Model):
	destinatario = models.ForeignKey(User, related_name='destinatario_user')
	data =  models.DateTimeField()
	testo = models.CharField(max_length=1000)
	letto = models.BooleanField()
	

class Log(models.Model):
	testo = models.CharField(max_length=50)
	data = models.DateTimeField()

class UserCreationForm2(UserCreationForm):
	email = forms.EmailField(label = "Email")
	class Meta:
		model = User
		fields = ("username", "email", )

class UserChangeForm2(UserChangeForm):
	class Meta:
		model = User
		fields = ("username", "email",)
	def clean_password(self):
		return "" # This is a temporary fix for a django 1.4 bug
		
class Impostazioni_notifica(models.Model):
	utente = models.ForeignKey(User, related_name='impostazioni_notifica_utente', limit_choices_to = {'is_staff':True})
	giorni = MultiSelectField(max_length=250, blank=True, choices=GIORNO)
	tipo_turno = models.ManyToManyField(TipoTurno, blank=True, null=True)

class Impostazioni_notificaForm(forms.ModelForm):
	giorni = MultiSelectFormField(choices=GIORNO)
	class Meta:
		model = Impostazioni_notifica
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('utente'),
			InlineCheckboxes('giorni'),
			InlineCheckboxes('tipo_turno'),
			FormActions(
				Submit('save', 'Aggiungi', css_class="btn-primary")
			)
		)
		super(Impostazioni_notificaForm, self).__init__(*args, **kwargs)
		self.fields['tipo_turno'].queryset = TipoTurno.objectsGet.all()
