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
	cur.execute("SELECT * FROM abilitazioni;")
	mansioni = cur.fetchall()
	mansioni_get = Mansione.objects.all()
	m_dict={}
	for a in mansioni: 
		try:
			m=Mansione.objects.get(id=a[0])
		except:
			m=Mansione(id=a[0])
		m.nome=a[1]
		m.descrizione=a[1]
		m.save()
		m_dict[a[0]]=m
	cur.execute("SELECT * FROM volontari;")
	persone_utenti = cur.fetchall()
	persone_get = Persona.objects.all()
	for a in persone_utenti:
		if a[12]==4 or a[12]==10:
			try:
				p=Persona.objects.get(id=a[0])
			except:
				p=Persona(id=a[0])
				esistente=True
			p.nome = a[2].title()
			p.cognome = a[1].title()
			p.indirizzo= a[4]+" "+a[5]+" "+a[6]+" "+a[7]
			p.nascita =  a[9]
			p.note = a[14]
			p.stato="disponibile"
			n=[16,17,15,18,19]
			tel=["","",""]
			k=0
			for i in n:
				if (a[i]!="" and a[i] and k<3):
					tel[k]=a[i]
					k=k+1
			if k==0:
				tel[0]="0"
			p.tel1,p.tel2,p.tel3=tel
			cur.execute("SELECT idabilitazione FROM abvolontari WHERE idvol="+str(a[0])+";")
			persona_abilitazioni=cur.fetchall()
			p.competenze.clear()
			for abilita in  persona_abilitazioni:
				p.competenze.add(m_dict[abilita[0]])
			p.save()
		else:
			try:
				p=Persona.objects.get(id=a[0])
				p.stato="indisponibile"
				p.save()
			except:
				pass

	#manca da associare le mansioni alle persone e gli utenti

