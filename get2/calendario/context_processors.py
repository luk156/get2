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
		##084B8A
		'titolo_color':  getattr(settings, 'GET_TITOLO_COLOR', '#FF4000'),
		'analytics': settings.GET_ANALYTICS,
		'dominio': settings.GET_DOMINIO,
		'js_personalizzato': getattr(settings, 'GET_JS', ''),
		'footer_site': getattr(settings, 'GET_FOOTER_SITE', 'www.gestionaleturni.it'),
		'footer_mail': getattr(settings, 'GET_FOOTER_MAIL', 'matteo@luccalug.it'),
		'footer_doc': getattr(settings, 'GET_FOOTER_DOC', 'documentazione.gestionaleturni.it'),
		'logo': getattr(settings, 'GET_LOGO', 'turnionline.png'),
		'app_name': getattr(settings, 'GET_APP_NAME', 'GeT'),
	}
