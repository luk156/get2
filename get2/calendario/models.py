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

class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple
 
    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', 0)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)
 
    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        # if value and self.max_choices and len(value) > self.max_choices:
        #     raise forms.ValidationError('You must select a maximum of %s choice%s.'
        #             % (apnumber(self.max_choices), pluralize(self.max_choices)))
        return value

 
class MultiSelectField(models.Field):
    __metaclass__ = models.SubfieldBase
 
    def get_internal_type(self):
        return "CharField"
 
    def get_choices_default(self):
        return self.get_choices(include_blank=False)
 
    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choicedict = dict(field.choices)
 
    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name),
                    'help_text': self.help_text, 'choices': self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value):
        return value

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, list):
            return ",".join(value)
 
    def to_python(self, value):
        if value is not None:
            return value if isinstance(value, list) else value.split(',')
        return ''

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname = name, choicedict = dict(self.choices): ",".join([choicedict.get(value, value) for value in getattr(self, fieldname)])
            setattr(cls, 'get_%s_display' % self.name, func)
 
    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if (int(opt_select) not in arr_choices):  # the int() here is for comparing with integer choices
                raise exceptions.ValidationError(self.error_messages['invalid_choice'] % value)  
        return
 
    def get_choices_selected(self, arr_choices=''):
        if not arr_choices:
            return False
        list = []
        for choice_selected in arr_choices:
            list.append(choice_selected[0])
        return list
 
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
        
from south.modelsinspector import add_introspection_rules  
add_introspection_rules([], ["^get2\.calendario\.models\.MultiSelectField"]) 

ICONE = (
	('icon-user','icon-user'),
	('icon-ambulance','icon-ambulance'),
	('icon-user-md','icon-user-md'),
	('icon-phone','icon-phone'),
	('icon-stethoscope','icon-stethoscope'),
	('icon-eye-open','icon-eye-open'),
	)

class Mansione(models.Model):
	nome =models.CharField('Nome',max_length=20)
	descrizione = models.TextField('Descrizione estesa')
	icona = models.TextField('Icona', choices=ICONE, default='icon-user' )
	colore = models.TextField('Colore', default='#aaa' )
	def __unicode__(self):
		return '%s' % (self.nome)
	# Milite tipo A, milite tipo B, centralinista ecc... 

class MansioneForm(forms.ModelForm):
	class Meta:
		model = Mansione
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('nome'),
			Field('descrizione'),
			Field(
				'colore',
				template = 'form_templates/color.html'
			),
			Field(
        		'icona',
				template = 'form_templates/radioselect_inline.html',
			),
			FormActions(
				Submit('save', 'Invia', css_class="btn-primary")
			)
		)
		super(MansioneForm, self).__init__(*args, **kwargs)

STATI=(('disponibile','Disponibile'),('ferie','In ferie'),('malattia','In malattia'),('indisponibile','Indisponibile'))

class Persona(models.Model):
	user = models.ForeignKey(User, unique=True, blank=True, null=True, related_name='pers_user')
	nome = models.CharField('Nome',max_length=200)
	cognome = models.CharField('Cognome',max_length=200)
	indirizzo = models.TextField( blank=True, null=True, )
	nascita = models.DateField('Data di nascita', blank=True, null=True,)
	tel1 = models.CharField('Telefono Principale',max_length=20)
	tel2 = models.CharField('telefono Secondario',max_length=20, blank=True, null=True)
	#caratteristiche della persona
	stato = models.CharField('Stato',max_length=40, choices=STATI, default='disponibile' )
	competenze = models.ManyToManyField(Mansione, blank=True, null=True)
	retraining = models.DateField('Ultimo retraining livello A')
	retraining_blsd = models.DateField('Ultimo retraining Operatore BLSD')
	note = models.TextField( blank=True, null=True, )
	def notifiche_non_lette(self):
		n=0
		for m in Notifica.objects.filter(destinatario=self.user):
			if(m.letto == False):
				n+=1
		return n
	def __unicode__(self):
		return '%s %s' % (self.cognome,self.nome)

class PersonaForm(forms.ModelForm):
	class Meta:
		model = Persona
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			HTML('<div class="row">'),
			Div(
				Fieldset(
					'Informazioni Anagrafiche',
					'nome',
					'cognome',
					'indirizzo',
					),
				AppendedText('nascita', '<i class="icon-calendar"></i>'),
				AppendedText('tel1', '<i class="icon-phone"></i>'),
				AppendedText('tel2', '<i class="icon-phone"></i>'),
				css_class="span3",
			),
			Div(
				Fieldset(
					'Altre informazioni',
					'user',
					'stato',
					),
				InlineCheckboxes('competenze', css_class="badge-mansione"),
				AppendedText('retraining', '<i class="icon-calendar"></i>'),
				AppendedText('retraining_blsd', '<i class="icon-calendar"></i>'),
				css_class="span3"
			),
			HTML('</div>'),
			FormActions(
				Submit('save', 'Invia', css_class="btn-primary"),
			)
		)
		super(PersonaForm, self).__init__(*args, **kwargs)


class Gruppo(models.Model):
	nome = models.CharField('Nome',max_length=30)
	componenti = models.ManyToManyField(Persona, blank=True, null=True, related_name='componenti_gruppo')
	note = models.TextField( blank=True, null=True, )
	def numero_componenti(self):
		n=0
		for c in self.componenti.all():
			n+=1
		return n
	def __unicode__(self):
		return '%s' % (self.nome)

class GruppoForm(forms.ModelForm):
	#nascita = forms.DateField(label='Data di nascita', required=False, widget=widgets.AdminDateWidget)
	class Meta:
		model = Gruppo
		exclude = ('componenti')
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('nome'),
			Field('note'),
			FormActions(
				Submit('save', 'Invia', css_class="btn-primary")
			)
		)
		super(GruppoForm, self).__init__(*args, **kwargs)

class TipoTurno(models.Model):
	identificativo = models.CharField(max_length=30, blank=False)
	def __unicode__(self):
		return '%s' % (self.identificativo)

class TipoTurnoForm(forms.ModelForm):
	class Meta:
		model = TipoTurno
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('identificativo'),
			FormActions(
				Submit('save', 'Invia', css_class="btn-primary")
			)
		)
		super(TipoTurnoForm, self).__init__(*args, **kwargs)

OPERATORI=(('=','Uguale a'),('>','Maggiore di'))

class Requisito(models.Model):
	mansione=models.ForeignKey(Mansione, related_name="req_mansione")
	operatore=models.CharField('operatore', max_length=10, choices=OPERATORI )
	valore=models.IntegerField()
	massimo=models.IntegerField(default=0)
	tipo_turno=models.ForeignKey(TipoTurno, related_name="req_tipo_turno",)
	necessario=models.BooleanField('Necessario')
	sufficiente=models.BooleanField('Sufficiente')
	extra=models.BooleanField('Extra')

class RequisitoForm(forms.ModelForm):
	class Meta:
		model = Requisito
		exclude = ('tipo_turno')
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('mansione'),
			Field('operatore'),
			Field('valore'),
			Field('massimo'),
			Field('necessario'),
			Field('sufficiente'),
			Field('extra'),
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
  (101, 'prefestivo'),
  (102, 'festivo'),
  (103, 'feriale'),
  (99, 'qualsiasi'),
  )

class Occorrenza(models.Model):
	pass


ops = {"=": operator.eq, ">": operator.gt}

class Turno(models.Model):
	identificativo = models.CharField(max_length=30, blank=True , default='')
	inizio = models.DateTimeField()
	fine = models.DateTimeField()
	tipo = models.ForeignKey(TipoTurno, blank=True, null=True, on_delete=models.SET_NULL)
	occorrenza = models.ForeignKey(Occorrenza, blank=True, null=True)
	valore = models.IntegerField('Punteggio',default=1)
	def verifica_requisito(self,requisito):
		#pdb.set_trace()
		if requisito.necessario:
			contatore=0
			for d in self.turno_disponibilita.filter(tipo="Disponibile").all():
				if (not requisito.extra and d.mansione==requisito.mansione):
					contatore+=1
				if (requisito.extra and requisito.mansione in d.persona.competenze.all()):
					contatore+=1
			operatore=ops[requisito.operatore]
			if not (operatore(contatore,requisito.valore)):
				return False
			if contatore>requisito.massimo and requisito.massimo!=0:
				return False
			return True
		else:
			return True
	def gia_disponibili(self,requisito):
		return self.turno_disponibilita.filter(tipo="Disponibile",mansione=requisito.mansione).count()
	def coperto(self):
		if self.tipo:
			for r in Requisito.objects.filter(tipo_turno=self.tipo_id):
				if not self.verifica_requisito(r):
					return False
				elif r.sufficiente:
					return True
		return True
	def contemporanei(self):
		i=self.inizio+datetime.timedelta(seconds=60)
		f=self.fine-datetime.timedelta(seconds=60)
		return Turno.objects.filter( (models.Q(inizio__lte=i) & models.Q(fine__gte=f)) | models.Q(inizio__range=(i ,f)) | models.Q(fine__range=(i,f)) ).exclude(id=self.id)
	def mansioni(self):
		return Mansione.objects.filter(req_mansione__tipo_turno=self.tipo)

class TurnoForm(forms.ModelForm):
	modifica_futuri=forms.BooleanField(label="modifica occorrenze future",required=False)
	modifica_tutti=forms.BooleanField(label="modifica tutte le occorrenze",required=False)
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
			FormActions(
				Submit('save', 'Modifica', css_class="btn-primary")
			)
		)
		super(TurnoForm, self).__init__(*args, **kwargs)
		self.fields['tipo'].required = True
	class Meta:
		model = Turno
		exclude = ('occorrenza')
	def clean(self):
		data = self.cleaned_data
		if data.get('inizio')>data.get('fine'):
			raise forms.ValidationError('Il turno termina prima di iniziare! controlla inizio e fine')
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
	def clean(self):
		data = self.cleaned_data
		ripeti=data.get('ripeti')
		da=data.get('ripeti_da')
		al=data.get('ripeti_al')
		if data.get('inizio')>data.get('fine'):
			raise forms.ValidationError('Il turno termina prima di iniziare! controlla inizio e fine')
		if ripeti and (da==None or al==None):
			raise forms.ValidationError('Specifica l\' intervallo in cui ripetere il turno')
		return data



DISPONIBILITA = (("Disponibile","Disponibile"),("Indisponibile","Indisponibile"),("Darichiamare","Da Richiamare"),("Nonrisponde","Non Risponde"),)

class Disponibilita(models.Model):
	tipo = models.CharField(max_length=20, choices=DISPONIBILITA)
	persona = models.ForeignKey(Persona, related_name='persona_disponibilita')
	ultima_modifica = models.DateTimeField()
	creata_da = models.ForeignKey(User, related_name='creata_da_disponibilita')
	turno = models.ForeignKey(Turno, related_name='turno_disponibilita')
	mansione = models.ForeignKey(Mansione, related_name='mansione_disponibilita',blank=True, null=True, on_delete=models.SET_NULL)
	class Meta:
		ordering = ['mansione']

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

