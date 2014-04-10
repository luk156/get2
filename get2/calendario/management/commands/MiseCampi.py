import psycopg2
from django.core.management.base import BaseCommand
from get2.calendario.models import Persona
from persone.models import Mansione
from django.conf import settings
import MySQLdb
from django.contrib.auth.models import User
import re


# you must create a Cursor object. It will let
#  you execute all the query you need
database = settings.DATABASES['default']
db = MySQLdb.connect(host=database['HOST'], user=database['USER'], passwd=database['PASSWORD'], db=database['NAME'])
cur_my = db.cursor() 

#stati della sincronizzazione
# INCORSO, TERMINATA

class Command(BaseCommand):
    def handle(self, *args, **options):
        cur_my.execute("SELECT * FROM sincronizza WHERE stato='INCORSO'; ")
        lock = len(cur_my.fetchall()) > 0
        if lock:
            print 'sincronizzazione in corso'
        else:
            cur_my.execute("INSERT INTO sincronizza (stato,progresso) VALUES ('INCORSO','start'); ")
	    db.commit()
            sync_id = cur_my.lastrowid
            conn = psycopg2.connect(host=settings.EXT_HOST,user=settings.EXT_USER,password=settings.EXT_PASS,database=settings.EXT_DB)
            cur = conn.cursor()
            cur.execute("SELECT * FROM abilitazioni;")
            mansioni = cur.fetchall()
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
            tot=len(persone_utenti)
            n_p=0
            for a in persone_utenti:
                cur_my.execute("UPDATE sincronizza SET progresso='%s / %s' WHERE id=%s; ",(n_p,tot,sync_id))
		db.commit()
                n_p=n_p+1
                cancellato=False
                if a[36] != None or a[30] != None:
                    cancellato=True
                if (a[12]==4 or a[12]==10) and not cancellato:
                    try:
                        p=Persona.objects.get(id=a[0])
                    except:
                        p=Persona(id=a[0])
                    p.nome = a[2].title()
                    p.cognome = a[1].title()
                    print a[1]
                    p.indirizzo= a[4]+" "+a[5]+" "+a[6]+" "+a[7]
                    p.nascita =  a[9]
                    p.note = a[14]
                    p.stato="disponibile"
                    n=[16,17,15,18,19]
                    tel=["","",""]
                    k=0
                    for i in n:
                        if (a[i]!="" and a[i] and k<3):
                            rep = re.compile( '\D*')
                            tel[k]= rep.sub('',a[i])
                            k=k+1
                    if k==0:
                        tel[0]="0"
                    p.tel1,p.tel2,p.tel3=tel
                    cur.execute("SELECT idabilitazione FROM abvolontari WHERE idvol="+str(a[0])+";")
                    persona_abilitazioni=cur.fetchall()
                    p.save()
                    p.competenze.clear()
                    for abilita in  persona_abilitazioni:
                        p.competenze.add(m_dict[abilita[0]])
                    if a[21] != '' and a[21] != None:
                        try:
                            u=User.objects.get(username=a[21])
                        except:
                            u=User.objects.create_user(a[21], a[20], 'paola03')
                        u.save()
                        try:
                            cur_my.execute("""UPDATE auth_user SET password = %s WHERE username = %s """, (a[22],a[21]) )
                            db.commit()
                        except:
                            pass
                        p.user=u
                    p.save()
                else:
                    try:
                        p=Persona.objects.get(id=a[0])
                        p.stato="indisponibile"
                        p.save()
                    except:
                        pass
            cur_my.execute("UPDATE sincronizza SET stato='COMPLETATO' WHERE id=%s; ", (sync_id))
            db.commit()
            print 'sincronizzazione terminata'


