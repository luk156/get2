from django.db import models
from django import forms
from django.contrib.auth.models import User
import operator, datetime
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import pdb

#############################################################

from django.utils.text import capfirst
from django.core import exceptions

#### import per eav #####
import os
project = os.path.basename(os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % project
import eav
from eav.forms import BaseDynamicEntityForm
from eav.models import Attribute

from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^eav\.fields\.EavDatatypeField"])
add_ignored_fields(["^eav\.fields\.EavSlugField"])

#### fine import eav ####

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


# needed for South compatibility

from south.modelsinspector import add_introspection_rules  
add_introspection_rules([], ["^get2\.calendario\.models\.MultiSelectField"])

############################################


class Mansione(models.Model):
	nome =models.CharField('Nome',max_length=20)
	descrizione = models.TextField('Descrizione estesa')
	def __unicode__(self):
		return '%s' % (self.nome)
	# Milite tipo A, milite tipo B, centralinista ecc... 

class MansioneForm(forms.ModelForm):
	class Meta:
		model = Mansione

STATI=(('disponibile','Disponibile'),('ferie','In ferie'),('malattia','In malattia'),('indisponibile','Indisponibile'))

class Persona(models.Model):
	user = models.ForeignKey(User, unique=True, blank=True, null=True, related_name='pers_user')
	nome = models.CharField('Nome',max_length=200)
	cognome = models.CharField('Cognome',max_length=200)
	#caratteristiche della persona
	stato = models.CharField('Stato',max_length=40, choices=STATI, default='disponibile' )
	competenze = models.ManyToManyField(Mansione, blank=True, null=True)
	note = models.TextField( blank=True, null=True, )
	def notifiche_non_lette(self):
		n=0
		for m in Notifica.objects.filter(destinatario=self.user):
			if(m.letto == False):
				n+=1
		return n
	def __unicode__(self):
		return '%s %s' % (self.nome,self.cognome)

class PersonaForm(BaseDynamicEntityForm):
	#nascita = forms.DateField(label='Data di nascita', required=False, widget=widgets.AdminDateWidget)
	def __init__(self, *args, **kwargs):
		super(PersonaForm, self).__init__(*args, **kwargs)
		lista_attributi = eav.models.Entity(Persona).get_all_attributes()
		#pdb.set_trace()
		# da finire
		for attributo in lista_attributi:
			if attributo.datatype == 'date':
	       			self.fields[attributo.slug].widget.attrs['class'] = 'campo_tipo_data'
	class Meta:
		model = Persona		
		widgets = {'competenze': forms.CheckboxSelectMultiple}

eav.register(Persona) #registro il Model Persona come associazione a eav

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

class TipoTurno(models.Model):
	identificativo = models.CharField(max_length=30, blank=False)
	def __unicode__(self):
		return '%s' % (self.identificativo)

class TipoTurnoForm(forms.ModelForm):
	class Meta:
		model = TipoTurno


OPERATORI=(('=','Uguale a'),('>','Maggiore di'))

class Requisito(models.Model):
	mansione=models.ForeignKey(Mansione, related_name="req_mansione")
	operatore=models.CharField('operatore', max_length=10, choices=OPERATORI )
	valore=models.IntegerField()
	tipo_turno=models.ForeignKey(TipoTurno, related_name="req_tipo_turno",)
	necessario=models.BooleanField('Necessario')
	sufficiente=models.BooleanField('Sufficiente')
	extra=models.BooleanField('Extra')

class RequisitoForm(forms.ModelForm):
	class Meta:
		model = Requisito
		exclude = ('tipo_turno')
GIORNO = (
  (0, 'lunedi'),
  (1, 'martedi'),
  (2, 'mercoledi'),
  (3, 'giovedi'),
  (4, 'venerdi'),
  (5, 'sabato'),
  (6, 'domenica'),)

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
			if not operatore(contatore,requisito.valore):
				return False
			return True
		else:
			return True
	def coperto(self):
		if self.tipo:
			for r in Requisito.objects.filter(tipo_turno=self.tipo_id):
				if not self.verifica_requisito(r):
					return False
				elif r.sufficiente:
					return True
		return True
	def contemporanei(self):
		i=self.inizio+datetime.timedelta(seconds=1)
		f=self.fine-datetime.timedelta(seconds=1)
		return Turno.objects.filter( (models.Q(inizio__lte=i) & models.Q(fine__gte=f)) | models.Q(inizio__range=(i ,f)) | models.Q(fine__range=(i,f)) ).exclude(id=self.id)
	def mansioni(self):
		return Mansione.objects.filter(req_mansione__tipo_turno=self.tipo)

class TurnoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(TurnoForm, self).__init__(*args, **kwargs)
		self.fields['tipo'].required = True
	inizio=forms.DateTimeField(widget=forms.SplitDateTimeWidget)
	fine=forms.DateTimeField(widget=forms.SplitDateTimeWidget)
	class Meta:
		model = Turno
		exclude = ('occorrenza')

class TurnoFormRipeti(TurnoForm):
	ripeti = forms.BooleanField(required=False)
	ripeti_da = forms.DateField(required=False)
	ripeti_al = forms.DateField(required=False)
	ripeti_il_giorno = forms.MultipleChoiceField(choices=GIORNO, widget=forms.CheckboxSelectMultiple(),required=False)
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
		widgets = {'tipo_turno': forms.CheckboxSelectMultiple}


#### Form per Attribute(eav) ####
class AttributeForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AttributeForm, self).__init__(*args, **kwargs)
		self.fields['name'].help_text = ''
		self.fields['datatype'].label = 'Tipo'
		self.fields['required'].label = 'Obbligatorio'

	class Meta:
		model = Attribute
		exclude = ('slug', 'site', 'slug', 'description', 'enum_group', 'type')
