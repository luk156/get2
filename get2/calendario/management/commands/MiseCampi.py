import psycopg2
from django.core.management.base import BaseCommand, CommandError
from get2.calendario.models import Persona, Turno, Disponibilita
from persone.models import Mansione
import datetime
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
	conn = psycopg2.connect("dbname=misecampi user=postgres password=paola host=127.0.0.1")
	cur = conn.cursor()
	cur.execute("SELECT * FROM mansioni;")
	mansioni = cur.fetchall()
	mansioni_get = Mansione.objects.all()
	# campi abilitazioni idabilitazione descrizione duratamesi limiteeta
	for a in mansioni: 
		try:
			m=Mansione.objects.get(id=a[0])
			m.nome=a[1]
			m.descrizione=a[1]
			#m.save()
			print m
		except:
			m=Mansione(id=a[0],nome=a[1],descrizione=a[1])
			#m.save()
			print m
	cur.execute("SELECT * FROM volontari;")
	persone = cur.fetchall()
	print len(persone)