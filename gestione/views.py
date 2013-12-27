from django.shortcuts import render
import json
from django.http import HttpResponse

# Create your views here.
def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

def numero_istanze(request,classe):
	classe=classe.replace("_",".")
	response_data = {}
	response_data['numero'] = get_class(classe).objects.all().count()
	return HttpResponse(json.dumps(response_data), content_type="application/json")