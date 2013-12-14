from django.conf import settings

def calendari(request):
    from get2.calendario.models import Calendario
    return {'calendari': Calendario.objects.all()}

def titolo(request):
	return {'titolo': settings.GET_TITOLO }

def analytics(request):
	return {'analytics': settings.GET_ANALYTICS }

def dominio(request):
	return {'dominio': settings.GET_DOMINIO }