from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail
from get2.calendario.models import Persona, Turno, Disponibilita
import datetime
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
	dataInizio = datetime.date.today()
	dataInizio = dataInizio + datetime.timedelta(days=1)
	dataFine = dataInizio + datetime.timedelta(days=7)
	disponibilita = Disponibilita.objects.filter(turno__inizio__range=(dataInizio, dataFine), tipo="Disponibile")
	listaMessaggi = ()
	for dis in disponibilita:
		differenzaGiorni = (dis.turno.inizio.date() - datetime.date.today()).days
		if(dis.persona.user and dis.persona.user.email):
			if(dis.persona.notificaMail and int(dis.persona.giorniNotificaMail) == differenzaGiorni):
				messaggio = 'Salve ' + dis.persona.nome + ', ti ricordo che in data ' + dis.turno.inizio.date().strftime('%d/%m/%Y') + ' dalle ore ' + dis.turno.inizio.time().strftime('%H:%M') + ' alle ore ' + dis.turno.fine.time().strftime('%H:%M') + ' dovrai effettuare un turno.'
				listaMessaggi += (('Get 2.0 - Avviso turno', messaggio, settings.GET_MAIL_NOTIFICA, [dis.persona.user.email]),)
	send_mass_mail(listaMessaggi)
