*************
Il calendario
*************

.. image:: img/calendario_menu.png
	:align: center

Il calendario è il contenitore dei :doc:`turni <turno>`, essi vengono rappresentati disposti su sette colonne in ordine cronologico.

 .. note::

	Se due turni inziano contemporaneamente verrannò ordinato secondo la priorità del :ref:`tipo di turno <tipo_turno-label>`

GeT può gestire più calendari contemporaneamente riconoscibili dalla medesima icona nel menu principale.

Visualizzazione del calendario
==============================

La visualizzazione del calendario varia secondo il seguente schema:

* Utente non loggato
* Utente semplice
* Membro dello staff

Calendario utente non loggato
-----------------------------

.. image:: img/calendario_sloggato.png
	:align: center

Se si accede al calendario senza prima aver effettuato il login non saranno visibili i nomi delle persone segnate. Saranno però già riconoscibili i turni coperti e non in base al loro colore (verde coperto, rosso non coperto).

Calendario utente semplice
--------------------------

.. image:: img/calendario_utente.png
	:align: center

Quando il calendario è visualizzato da un utente semplice dopo aver effettuato il login appariranno i nomi delle persone già segnate e tutti i turni diventeranno clickabili.

.. image:: img/utente_disponibilita.png
	:align: center

Facendo click su un turno è possibili modificare la propria disponibilità. Se la modifica avviene entro i tempi preimpostati verrà mostrata una finestra di dialogo che permetterà all'utente di selezionare la mansione che vuole ricoprire. Se il click avviene su un turno per cui l'utente si è già reso disponbile egli sarà in grado di cancellarsi. In entrambi i casi verrà inviata una :doc:`notifica <notifiche>` all'utente dello staff predisposto.

 .. note::
 	I limiti temporali entro cui è possibile segnarsi o cancellarsi da un turno vengono impostati all' interno di un file di configurazione predefinito

 .. note::
 	La mansioni che saranno mostrate all'utente per potersi segnare vengono selezionate dal software in modo che non vadano in conflitto con i requisiti pre-impostati (se ad esempio è necessario massimo una autista e un utente si è già segnato nessun altro potrà farlo)

Calendario per lo staff
-----------------------

.. image:: img/calendario_staff.png
	:align: center

Quando è stato effettuato il login come menbro dello staff la visualizzazione del calendario risulta completa di tutte le informazioni sia sulle persone disponibili sia dei requisiti del singolo turno.

La visualizzazione del turno per i membri dello staff è la seguente:

.. image:: img/turno.png
	:align: center

All'interno del turno appaiono tutte le mansioni e sulla destra sono indicati i requisiti numerici all'interno di un badge colorato |E|. Esso può essere dei seguenti colori:

* **verde**: requisito soddisfatto
* **rosso**: requisito non soddisfatto
* **blu**: requisito sufficiente
* **grigio**: requisito non necessario

Facendo click sul badge si aprirà la pagina di ricerca delle persone per quella mansione. si veda la sezione :doc:`disponibilità <disponibilita>` per ulteriori informazioni.

 .. note::
 	se un requisito è indicato come *extra* apparirà un asterisco alla sua sinistra

 .. note::
 	se un requisito è indicato come *nascosto* non risulterà clickabile e sarà visibile solo allo staff

Nella parte superiore del turno sono indicate l'ora di inizio e fine del turno |A| ed un identificativo opzionale |D|.

Sono inoltre presenti due bottoni: il primo |B| richiama la pagina di modifica della disponibilità per un gruppo (si faccia ulteriore riferimento alla sezione :doc:`disponibilità <disponibilita>`) ed il secondo |C| permette di modificare o eliminare il turno.


Infine in basso |F| è riportata la tipologia del turno. 


Filtrare i giorni
=================

Tramite il bottone in alto a destra "FILTRA" è possibile visualizzare solo determinati giorni della settimana, i giorni feriali, prefestivi o festivi.

.. |A| image:: img/A.png
.. |B| image:: img/B.png
.. |C| image:: img/C.png
.. |D| image:: img/D.png
.. |E| image:: img/E.png
.. |F| image:: img/F.png