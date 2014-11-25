from django.db import models
from django import forms
# Create your models here.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *
import calendar,datetime,locale
from persone.models import Mansione, Gruppo
from get2.calendario.models import TipoTurno
from dateutil.relativedelta import relativedelta

class FiltroStatistiche(forms.Form):
	lista_gruppi = [('all','senza gruppo')]
	lista_mansioni = Mansione.objects.exclude(escludi_stat=True).values_list('id','nome')
	lista_gruppi += Gruppo.objects.exclude(escludi_stat=True).values_list('id','nome')
	lista_tipi_turno = TipoTurno.objectsGet.all().values_list('id','identificativo')
	mansioni = forms.MultipleChoiceField( label = "",	choices = lista_mansioni, initial = [x[0] for x in lista_mansioni], required = False,  widget = forms.CheckboxSelectMultiple,)
	tipi_turno = forms.MultipleChoiceField( label = "",	choices = lista_tipi_turno,initial = [x[0] for x in lista_tipi_turno],  required = False,  widget = forms.CheckboxSelectMultiple,)
	gruppi = forms.MultipleChoiceField( label = "",	choices = lista_gruppi,initial = [x[0] for x in lista_gruppi],  required = False,  widget = forms.CheckboxSelectMultiple,)
	start =  forms.DateField(label = "dal:", required = False, initial=(datetime.datetime.now() + relativedelta( years = -1 )).strftime("%d/%m/%Y"))
	stop = forms.DateField(label = "al:", required = False, initial=datetime.datetime.now().date().strftime("%d/%m/%Y"))
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_id = 'FiltroStatistiche'
		self.helper.layout = Layout(
			
			Field('start', type="hidden"),
			Field('stop', type="hidden"),
			HTML('<div class="row">'),
			Div(
				Fieldset('<h7>Tipologie di turno</h7>',
					InlineCheckboxes('tipi_turno', css_class="tipi_turno"),
				),
				css_class="span2",
			),
			Div(
				Fieldset('<h7>Mansioni</h7>',
					InlineCheckboxes('mansioni', css_class="mansioni"),
				),
				css_class="span2",
			),	
			Div(
				Fieldset('<h7>Gruppi</h7>',
					InlineCheckboxes('gruppi', css_class="gruppi"),
				),
				css_class="span2",
			),
			HTML('</div></br>'),
			
			Button('save', 'Filtra', onclick="aggiorna_statistiche();", css_class="btn-primary btn-small"),
			Button('cancel', 'Annulla', onclick="reset();", css_class="btn-small"),
			
			)
		self.helper.form_method = 'post'
		#self.helper.form_action = 'submit_survey'
		super(FiltroStatistiche, self).__init__(*args, **kwargs)
