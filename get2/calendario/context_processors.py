from django.conf import settings
from get2.calendario.models import Notifica

def calendari(request):
    from get2.calendario.models import Calendario
    return {'calendari': Calendario.objects.all()}

def notifiche_non_lette(request):
	n=0
	if request.user.is_staff:
		n=Notifica.objects.filter(destinatario=request.user,letto=False).count()
	return {'notifiche_non_lette': n}


def get_settings(request):
	return {
		'titolo': getattr(settings, 'GET_TITOLO', ''),
		'titolo_color':  getattr(settings, 'GET_TITOLO_COLOR', '#084B8A'),
		'analytics': getattr(settings, 'GET_ANALYTICS', ''),
		'dominio': getattr(settings, 'GET_DOMINIO', ''),
		'js_personalizzato': getattr(settings, 'GET_JS', ''),
		'footer_site': getattr(settings, 'GET_FOOTER_SITE', 'www.gestionaleturni.it'),
		'footer_mail': getattr(settings, 'GET_FOOTER_MAIL', 'matteo@luccalug.it'),
		'footer_doc': getattr(settings, 'GET_FOOTER_DOC', 'documentazione.gestionaleturni.it'),
		'logo': getattr(settings, 'GET_LOGO', ''),
		'app_name': getattr(settings, 'GET_APP_NAME', 'GeT'),
		'get_distingui_dipendenti': getattr(settings, 'GET_DISTINGUI_DIPENDENTI', False),
		'get_sovrascrivi_punteggio': getattr(settings, 'GET_SOVRASCRIVI_PUNTEGGIO', False),
	}
