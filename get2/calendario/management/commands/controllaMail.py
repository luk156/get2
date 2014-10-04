from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail
from get2.calendario.models import Persona, Turno, Disponibilita
import datetime
from django.conf import settings
import urllib
import urllib2
import re

def UrlEncode(recipients):
	resultString = ''
	for number in recipients:
			resultString = resultString + 'recipients[]=' + urllib.quote_plus(number) + '&'
	return resultString[:-1]

def skebbyGatewaySendSMS(username,password,recipients,text,sms_type='basic',sender_number='',sender_string='',charset='ISO-8859-1',options={ 'User-Agent' : 'Generic Client' }):
	url = 'http://gateway.skebby.it/api/send/smseasy/advanced/http.php'

	method = 'send_sms_basic'

	if sms_type=='classic' : method = 'send_sms_classic'
	if sms_type=='report' : method = 'send_sms_classic_report'

	parameters = {
			'method' : method,
			'username' : username,
			'password' : password,
			'text' : text
	}

	if sender_number != '' and sender_string != '' :
			result = {}
			result['status'] = 'failed'
			result['message'] = SENDER_ERROR
			return result

	if sender_number != '' : parameters['sender_number'] = sender_number
	if sender_string != '' : parameters['sender_string'] = sender_string

	if charset != 'ISO-8859-1' : parameters['charset'] = 'UTF-8'

	headers = options
	data = urllib.urlencode(parameters) + '&' + UrlEncode(recipients)

	req = urllib2.Request(url, data, headers)
	try:
			response = urllib2.urlopen(req)
	except urllib2.HTTPError as e:
			result = {}
			result['status'] = 'failed'
			result['code'] = e.code
			result['message'] = NET_ERROR
			return result
	except urllib2.URLError as e:
			result = {}
			result['status'] = 'failed'
			result['message'] = e.reason
			return result

	resultString = response.read()

	results = resultString.split('&')
	result = {}
	for r in results:
			temp = r.split('=')
			result[temp[0]] = temp[1]

	return result

class Command(BaseCommand):
	def handle(self, *args, **options):
		dataInizio = datetime.date.today()
		dataInizio = dataInizio + datetime.timedelta(days=1)
		dataFine = dataInizio + datetime.timedelta(days=7)
		disponibilita = Disponibilita.objects.filter(turno__inizio__range=(dataInizio, dataFine), tipo="Disponibile")
		listaMessaggi = ()
		cell_rule = re.compile('^[3]\d{9}$')
		for dis in disponibilita:
			differenzaGiorni = (dis.turno.inizio.date() - datetime.date.today()).days
			if(dis.persona.user and int(dis.persona.giorniNotificaMail) == differenzaGiorni):
				messaggio = 'Salve ' + dis.persona.nome + ', ti ricordo che in data ' + dis.turno.inizio.date().strftime('%d/%m/%Y') + ' dalle ore ' + dis.turno.inizio.time().strftime('%H:%M') + ' alle ore ' + dis.turno.fine.time().strftime('%H:%M') + ' dovrai effettuare un turno.'
				if(dis.persona.user.email != '' and dis.persona.notificaMail):
					listaMessaggi += (('Get 2.0 - Avviso turno', messaggio, settings.GET_MAIL_NOTIFICA, [dis.persona.user.email]),)

				if(getattr(settings, 'GET_ACTIVATE_SMS', False) and cell_rule.search(dis.persona.tel1) and dis.persona.notificaSMS):
					recipients=[]
					recipients.append('39'+dis.persona.tel1)
					result = skebbyGatewaySendSMS(getattr(settings, 'GET_SKEBBY_USERNAME', ""),getattr(settings, 'GET_SKEBBY_PASSWORD', ""),recipients,messaggio,'classic','',getattr(settings, 'GET_SMS_ALIAS', "GeT"))
					print result
		send_mass_mail(listaMessaggi)
