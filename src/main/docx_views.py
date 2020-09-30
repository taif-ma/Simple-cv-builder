
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from main.models import Cv
import pdfkit
from django.template import loader
from src.settings import BASE_DIR
import pypandoc

def download_docx(request, pk):
    cv = Cv.objects.get(pk=pk)
    
    user = request.user
    
    out = loader.render_to_string('cv-templates/%s.html' % cv.template, {'user':user, 'cv':cv})
    path = 'media/%s.docx' % cv.id
   
    pypandoc.convert_text(out,'docx', format='html', outputfile=path)

    absp = '%s/%s' % (BASE_DIR,path)
    with open(absp,'rb') as f:
        out = f.read()

    response = HttpResponse(out,content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    

    return response
   