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
		'titolo': settings.GET_TITOLO,
		'analytics': settings.GET_ANALYTICS,
		'dominio': settings.GET_DOMINIO,
		'js_personalizzato': settings.GET_JS,
		'footer_site': settings.GET_FOOTER_SITE,
		'footer_mail': settings.GET_FOOTER_MAIL,
		'footer_doc': settings.GET_FOOTER_DOC,
	}
