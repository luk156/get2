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

    easy_install django-crispy-forms django-dajax django-dajaxice south
    
oppure con `pip` con il comando:

    pip install django-crispy-forms django-dajax django-dajaxice south

##Screenshot

![Calendario](http://matteo.luccalug.it/wp-content/uploads/2013/03/calendario.png "Calendario")

![Cerca](http://matteo.luccalug.it/wp-content/uploads/2013/03/cerca.png "Ricerca persone")
