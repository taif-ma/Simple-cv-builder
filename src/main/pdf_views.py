
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from main.models import Cv
import pdfkit
from django.template import loader
from src.settings import BASE_DIR

def download_pdf(request, pk):
    cv = Cv.objects.get(pk=pk)
    
    user = request.user
   
    out = loader.render_to_string('cv-templates/%s.html' % cv.template, {'user':user, 'cv':cv})
    path = '%s.pdf' % cv.id
    pdfkit.from_string(out, path)
    #import pdb; pdb.set_trace()
    absp = '%s/%s' % (BASE_DIR,path)
    with open(absp,'rb') as f:
        out = f.read()
    return HttpResponse(out,'application/pdf')
