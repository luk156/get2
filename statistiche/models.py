from django.db import models
from django import forms
# Create your models here.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, HTML, Button
from crispy_forms.bootstrap import *
import calendar,datetime,locale
from persone.models import Mansione, Gruppo

class FiltroStatistiche(forms.Form):
	lista_gruppi = [('all','senza gruppo')]
	lista_mansioni = Mansione.objects.all().values_list('id','nome')
	lista_gruppi += Gruppo.objects.all().values_list('id','nome')
	mansioni = forms.MultipleChoiceField( label = "",	choices = lista_mansioni, initial = [x[0] for x in lista_mansioni], required = False,  widget = forms.CheckboxSelectMultiple,)
	gruppi = forms.MultipleChoiceField( label = "",	choices = lista_gruppi,initial = [x[0] for x in lista_gruppi],  required = False,  widget = forms.CheckboxSelectMultiple,)
	start =  forms.DateField(label = "dal:", required = False, initial=datetime.date(datetime.datetime.today().year,1,1))
	stop = forms.DateField(label = "al:", required = False, initial=datetime.datetime.now().date())
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_id = 'FiltroStatistiche'
		self.helper.layout = Layout(
			HTML('<div class="row">'),
			Div(
				Fieldset('<h6>Data</h6>',
				AppendedText('start', '<i class="icon-calendar"></i>', css_class="dateinput span4"),
				AppendedText('stop', '<i class="icon-calendar"></i>',  css_class="dateinput span4"),
				),
				css_class="span3",
			),
			Div(
				Fieldset('<h6>Mansioni</h6>',
					InlineCheckboxes('mansioni', css_class="mansioni"),
				),
				Fieldset('<h6>Gruppi</h6>',
					InlineCheckboxes('gruppi', css_class="gruppi"),
				),
				css_class="span3",
			),
			HTML('</div>'),
			FormActions(
			    Button('save', 'Filtra', onclick="aggiorna_statistiche();", css_class="btn-primary"),
			    Button('cancel', 'Annulla', onclick="reset();"),
			),
			)
		self.helper.form_method = 'post'
		#self.helper.form_action = 'submit_survey'
		super(FiltroStatistiche, self).__init__(*args, **kwargs)