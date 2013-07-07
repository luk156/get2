
def calendari(request):
    from get2.calendario.models import Calendario
    return {'calendari': Calendario.objects.all()}