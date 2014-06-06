from get2.calendario.models import *
from datetime import date
import json
import simplejson
from django.forms.models import model_to_dict

def ajax_request_manager(control,type,data,request):
	res = {}
	if control == 'calendar':
		if type == 'init':
			start = date.fromtimestamp(float(data['start']))
			stop = date.fromtimestamp(float(data['stop']))
			calendario = []
			c=Calendario.objects.get(id=1)
			while start<stop + datetime.timedelta(days=1):
				giorno = {}
				giorno['data']=start.isoformat()
				giorno['turni']=[]
				Turni = Turno.objects.filter(inizio__range=(start, start + datetime.timedelta(days=1)),calendario=c).order_by('inizio', 'tipo__priorita')
				for turno in Turni:
					t={}
					t['id'] = turno.id
					t['inizio'] = turno.inizio.isoformat()
					t['fine'] = turno.fine.isoformat()
					t['requisiti'] = []
					for cache_r in turno.cache_requisito_set.all():
						r=model_to_dict(cache_r.requisito)
						r['mansione'] = model_to_dict(cache_r.requisito.mansione)
						r['verificato'] = cache_r.verificato
						r['disponibilita'] = []
						for disp in cache_r.disponibilita.all():
							p = str(disp.persona)
							r['disponibilita'].append(p)
						t['requisiti'].append(r)
					giorno['turni'].append(t)
				start = start + datetime.timedelta(days=1)
				calendario.append(giorno)
			print calendario
			return simplejson.dumps(calendario)
	return res
