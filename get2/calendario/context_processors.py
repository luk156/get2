import get2.calendario.settings_calendario as settings_calendario

def calendari(request):
    from get2.calendario.models import Calendario
    return {'calendari': Calendario.objects.all()}

def titolo(request):
	return {'titolo': settings_calendario.TITOLO }