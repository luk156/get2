# Il progetto è deprecato in favore di https://www.apptome.it

#get2

GeT nasce per semplificare la gestione di tutte quelle attività che prevedono dei turni, in particolare nasce da un lavoro congiunto con una pubblica assistenza.

Il programma web permette agli addetti ai turni di vedere quali sono i turni ancora da coprire e trovare più facilmente le persone disponibili a svolgere determinate mansioni.

Il software è completamente personalizzabile e può essere adattato ai più disparati ambiti, dal settore commerciale a qualsiasi altra attività che preveda dei turni.

##caratteristiche principali

*	Il software è sviluppato come una applicazione web: cioè può essere utilizzato su qualsiasi PC, Mac, Tablet ec.. che abbia la possibilità di collegarsi ad internet senza dover installare alcunché;
*	Il lavoro dei responsabili dei turni può essere effettuato anche da casa, lavorando su un calendario sempre aggiornato;
*	Le persone sono in grado di controllare da casa il calendario dei turni e di rendersi eventualmente disponibili per ricoprire una mansione;
*	Il programma dispone di un sistema di statistiche personalizzabile aggiornate in tempo reale;

##Come funziona?

GeT si occupa innanzitutto di archiviare una anagrafica delle persone fornendo all'amministratore la possibilità di inserire informazioni rispetto alla mansioni che ogni singola persona è in grado di svolgere. Le mansioni posso essere create a piacimento a seconda delle esigenze.

In base alla mansioni che sono state create all'interno del programma è possibile definire delle tipologie di turno con requisiti basati proprio su quest'ultime. Esempio: il numero di militi deve essere maggiore di 2.

A questo punto possono essere creati i turni di cui ho bisogno, fornendo l'orario e la tipologia di turno. Un volta che il turno è stato creato l'amministratore sarà in grado di aggiungere delle disponibilità che potranno essere sia favorevoli che no, in modo che anche gli altri responsabili possano sapere se una persona ha già dichiarato di non essere disponibile per quel turno.

Le persone dotate di un account hanno la possibilità di vedere da casa chi è già inserito all'interno del calendario ma possono anche rendersi disponibili o cancellarsi da un turno autonomamente.

##Componenti da installare

Per funzionare correttamente GeT necessita dei seguenti componenti aggiuntivi da installare:

*   django-crispy-forms
*   django-dajax
*   django-dajaxice
*   south

I componenti sono installabili con `easy_install` con il seguente comando:

    easy_install django-crispy-forms django-dajax django-dajaxice south python-dateutil
    
oppure con `pip` con il comando:

    pip install django-crispy-forms django-dajax django-dajaxice south python-dateutil

##Screenshot

![Calendario](http://matteo.luccalug.it/wp-content/uploads/2013/03/calendario.png "Calendario")

![Cerca](http://matteo.luccalug.it/wp-content/uploads/2013/03/cerca.png "Ricerca persone")

##Impostazioni

Titolo e colore dell'installazione

    GET_TITOLO="demo"
    GET_TITOLO_COLOR="#084B8A"

 Giorni disponibili per creare o eliminare una disponibilita da parte di una persona

    GET_DISP_MIN=1
    GET_DISP_MAX=60
    
    GET_CANC_MIN=2
    GET_CANC_MAX=0

Id dell' utente amministratore a cui inviare le notifiche che non avrebbero altro destinatario

    GET_ID_ADMIN_NOTIFICHE=1
Se True vengono inviate all'amministratore anche le notifiche riguardo le disponibilità create dallo staff

    GET_NOTIFICA_ALL=False

Codice e dominio per monitorare l'applicazione con Analytics

    GET_ANALYTICS="UA-1111111-1"
    GET_DOMINIO="gestionaleturni.it"

Indirizzo mail con cui vengono inviate le notifiche SMS

    GET_MAIL_NOTIFICA = "no@no.it"

Parametro necessario per creare l'url di recupero password

    SITE_ID = 1

Nome del file Javascript che può essere incorporato in un'installazione per sovrascrivere comportamenti standard di GeT

    GET_JS = ""

Informazione relative all'applicazione

    GET_APP_NAME="GeT"
    GET_LOGO=""
    GET_FOOTER_SITE="www.gestionaleturni.it"
    GET_FOOTER_MAIL="matteo@luccalug.it"
    GET_FOOTER_DOC="documentazione.gestionaleturni.it"

Impostazione per la notifica SMS

    GET_ACTIVATE_SMS=False
    GET_SKEBBY_USERNAME=""
    GET_SKEBBY_PASSWORD=""

Impostazione per ignorare il controllo che evita che una medesima persona sia segnata a due turni contemporanei

    GET_IGNORA_CONTEMPORANEI=False

Impostazione per abilitare la validazione della password degli utenti (8caratteri,un numero,una maiscola)

    GET_SECURE_PASSWORD=True

Possibilità di distinguere le persone tra dipendenti e non, per il momento permette solo di avere delle statistiche separate

    GET_DISTINGUI_DIPENDENTI=False

Possibilità di sovrascrivere il punteggio raccolto da una persone per lo svolgimento di un servizio

    GET_SOVRASCRIVI_PUNTEGGIO=False
