
from django.db import models
from django import forms
from django.contrib.auth.models import User
import operator, datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML
from crispy_forms.bootstrap import *
from django.utils.text import capfirst
from django.db.models import Q
from django.utils.functional import cached_property


class GetModelManager(models.Manager):
    def get_query_set(self):
        return super(GetModelManager, self).get_query_set().filter(cancellata=False)

# Create your models here.

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

class SelfForeignKey(models.ForeignKey):
    def pre_save(self, instance, add):
        manager = instance.__class__.objects
        ancestor_id = getattr(instance, self.attname)
        while ancestor_id is not None:
            if ancestor_id == instance.id:
                return None
            ancestor = manager.get(id=ancestor_id)
            ancestor_id = getattr(ancestor, self.attname)
        return getattr(instance, self.attname)
        
from south.modelsinspector import add_introspection_rules  
add_introspection_rules([], ["^persone\.models\.MultiSelectField"]) 
add_introspection_rules([], ["^persone\.models\.SelfForeignKey"]) 

STATI=(('disponibile','Disponibile'),('ferie','In ferie'),('malattia','In malattia'),('indisponibile','Indisponibile'))

GIORNI=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'))

ICONE = (
    ('icon-user','icon-user'),
    ('icon-ambulance','icon-ambulance'),
    ('icon-truck','icon-truck'),
    ('icon-user-md','icon-user-md'),
    ('icon-phone','icon-phone'),
    ('icon-stethoscope','icon-stethoscope'),
    ('icon-eye-open','icon-eye-open'),
    ('icon-bolt','icon-bolt'),
    ('icon-male','icon-male'),
    ('icon-female','icon-female'),
    )

class Mansione(models.Model):
	nome =models.CharField('Nome',max_length=30)
	descrizione = models.TextField('Descrizione estesa', null=True, blank=True)
	icona = models.TextField('Icona', choices=ICONE, default='icon-user' )
	colore = models.TextField('Colore', default='#aaa' )
	padre=SelfForeignKey('self', null=True, blank=True, related_name='children')
	escludi_stat = models.BooleanField('Escludi dalle statistiche', default=False,  help_text="Le disponibilita per questa mansione saranno escluse dalle statistiche")
	ereditabile = models.BooleanField('Ereditabile', default=True,  help_text="Le persone con una mansione superiore erediteranno automaticamente questa mansione")
	#cancellata =  models.BooleanField(default=False )
	#objects = GetModelManager()
	def __unicode__(self):
		return '%s' % (self.nome)
	# Milite tipo A, milite tipo B, centralinista ecc...
	def root(self):
		if self.padre:
			return False
		return True

def figli(mansione_id):
    mansioni = Mansione.objects.all().values_list('id','padre')
    f = [v for i, v in enumerate(mansioni) if v[1] == mansione_id]
    figli_list = f
    while f:
        for k in f:
            f=[v for i, v in enumerate(mansioni) if v[1] == k[0]]
            figli_list+=f
    return Mansione.objects.filter( id__in=[x for (x,y) in figli_list] )



class MansioneForm(forms.ModelForm):
    class Meta:
        model = Mansione
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nome'),
            Field('descrizione'),
            Field('padre'),
            Field(
                'colore',
                template = 'form_templates/color.html'
            ),
            Field(
                'icona',
                template = 'form_templates/radioselect_inline.html',
            ),
            Field('escludi_stat'),
            Field('ereditabile'),
            FormActions(
                Submit('save', 'Invia', css_class="btn-primary")
            )
        )
        super(MansioneForm, self).__init__(*args, **kwargs)
        self.fields['padre'].queryset = Mansione.objects.exclude(id__exact=self.instance.id)


class Persona(models.Model):
	user = models.OneToOneField(User, unique=True, blank=True, null=True, related_name='pers_user')
	nome = models.CharField('Nome',max_length=200)
	cognome = models.CharField('Cognome',max_length=200)
	indirizzo = models.TextField('Indirizzo', blank=True, null=True, )
	nascita = models.DateField('Data di nascita', blank=True, null=True,)
	tel1 = models.CharField('Telefono Principale',max_length=30)
	tel2 = models.CharField('Telefono Secondario',max_length=30, blank=True, null=True, default="")
	tel3 = models.CharField('Altro telefono',max_length=30, blank=True, null=True, default="")
	#caratteristiche della persona
	stato = models.CharField('Stato',max_length=40, choices=STATI, default='disponibile' )
	competenze = models.ManyToManyField(Mansione, blank=True, null=True)
	note = models.TextField( blank=True, null=True, )
	notificaMail = models.BooleanField('Attiva', default=False )
	giorniNotificaMail = models.PositiveSmallIntegerField('Giorni di anticipo', choices=GIORNI, default=2, blank=True, null=True )
	cancellata = models.BooleanField(default=False )
	objects = GetModelManager()
	def notifiche_non_lette(self):
		return self.user.destinatario_user.filter(letto=False).count()
	@cached_property
	def telefono(self):
		tel_fields = filter(bool, [self.tel1, self.tel2, self.tel3])
		return '<br>'.join(tel_fields)
	@cached_property
	def autista_cv(self):
		try:
			self.competenze.get(id=6)
			return True
		except:
			return False
	@cached_property
	def capacita(self):
		c = set()
		for m in self.competenze.all():
			c.add(m)
			for f in figli(m.id):
				if (f.ereditabile):
					c.add(f)
		return c

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
                AppendedText('tel3', '<i class="icon-phone"></i>'),
                css_class="span3",
            ),
            Div(
                Fieldset(
                    'Altre informazioni',
                    'user',
                    'stato',
                    ),
                InlineCheckboxes('competenze', css_class="badge-mansione"),
                css_class="span3"
            ),
            Fieldset(
                'Notifiche via E-mail',
                'notificaMail',
                AppendedText('giorniNotificaMail', '<i class="icon-envelope"></i>'),
                ),
            HTML('</div>'),
            FormActions(
                Submit('save', 'Invia', css_class="btn-primary"),
            )
        )
        super(PersonaForm, self).__init__(*args, **kwargs)

class PersonaFormLite(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ('competenze', 'user')
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
                AppendedText('tel3', '<i class="icon-phone"></i>'),
                css_class="span3",
                ),
            Div(
                Fieldset(
                    'Altre informazioni',
                    'stato',
                    ),
                css_class="span3"
            ),
            Fieldset(
                'Notifiche via E-mail',
                'notificaMail',
                AppendedText('giorniNotificaMail', '<i class="icon-envelope"></i>'),
                ),
            HTML('</div>'),
            FormActions(
                Submit('save', 'Invia', css_class="btn-primary"),
                )
        )
        super(PersonaFormLite, self).__init__(*args, **kwargs)

class Gruppo(models.Model):
    nome = models.CharField('Nome',max_length=30)
    componenti = models.ManyToManyField(Persona, blank=True, null=True, related_name='componenti_gruppo')
    note = models.TextField( blank=True, null=True, )
    escludi_stat = models.BooleanField('Escludi dalle statistiche', default=False,  help_text="le persone appartenenti a questo gruppo saranno escluse dalle statistiche")
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
        exclude = ('componenti',)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nome'),
            Field('note'),
            Field('escludi_stat'),
            FormActions(
                Submit('save', 'Invia', css_class="btn-primary")
            )
        )
        super(GruppoForm, self).__init__(*args, **kwargs)

