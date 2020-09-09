import logging
from django.contrib.auth.models import Group
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django_slugify_processor.text import slugify
from users.forms import CustomUserChangeForm
from .forms import *
from .models import *

import ssl
from django.shortcuts import redirect

ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



FORMS = [('cvs', CvForm),
         ('work_experience', WorkExperienceForm),
         ('education', EducationForm),
         ('certifications', CertificationForm),
         ('courses', CourseFormSet),
         ('projects', ProjectFormSet),
         ('publication', PublicationFormSet),
         ('skills', SkillFormSet),
         ('languages', LanguageFormSet),
         ('hobbies', HobbyFormSet),
         ('custom_section', CustomFormSet),
          ]

FORM_TYPES = ('work_experience', 'education', 'certifications', 'courses', 'projects', 'publications', 'skills', 'languages', 'hobbies')

TEMPLATES = {'cvs': 'cv-forms/cvs.html',
             'work_experience': 'cv-forms/cv_experience.html',
             'education': 'cv-forms/cv_education.html',
             'certifications': 'cv-forms/cv_certifications.html',
             'projects': 'cv-forms/cv_projects.html',
             'skills': 'cv-forms/cv_skills.html',
             'languages': 'cv-forms/cv_languages.html',
             'publication': 'cv-forms/cv_publications.html',
             'courses': 'cv-forms/cv_courses.html',
             'hobbies': 'cv-forms/cv_hobbies.html',
             'custom_section': 'cv-forms/cv_custom_section.html',
              }




def add_cv(request):
    user = request.user
    form = CvForm()
    #cv = Cv.object.get(pk=pk)
    if request.method == 'POST':
        form = CvForm(request.POST)
        if form.is_valid():
            name= form.cleaned_data.get("name")
            sections= form.cleaned_data.get("sections")
            template= form.cleaned_data.get("template")
            form.save(commit=False)
            cv = Cv()
            cv.name = name
            cv.sections = sections
            cv.template = template
            cv.user = user
            cv.save()
            #updated_values= {'name':cv.name,'sections':cv.sections}
            #obj, created = Cv.objects.update_or_create(user=user,name=name, defaults=updated_values)
            #pk = cv.id
            section = sections[0]

            return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':cv.pk}))
          
            
            
        else:
            form = CvForm()
    else:
        form = CvForm()  
        
    return render(request,'cv-forms/cvs.html',{'form':form, 'user':user})

########## Work Experience
@login_required
def work_experience(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    objs = []
    for exp in WorkExperience.objects.filter(cv=cv):
        objs.append({'cv': exp.cv, 'position': exp.position, 'company': exp.company, 'achievements': exp.achievements, 'city': exp.city, 'start_date': exp.start_date, 'end_date': exp.end_date, 'id': exp.id})
    WorkExperienceFormSet = formset_factory(WorkExperienceForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        experience_formset = WorkExperienceFormSet(request.POST)
        for form in experience_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            section = sections[sections.index('work_experience') + 1]
            return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))       
    
    else:
        experience_formset = WorkExperienceFormSet(initial=objs)

    return render(request,'cv-forms/cv_experience.html',{'experience_formset':experience_formset, 'user':user, 'cv': cv})


########## Education
@login_required
def education(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    sections_len = len(sections)-1

    objs = []
    for edu in Education.objects.filter(cv=cv):
        objs.append({'cv': edu.cv, 'school': edu.school, 'department': edu.department, 'degree': edu.degree, 'major': edu.major, 'city': edu.city, 'description': edu.description, 'start_date': edu.start_date, 'end_date': edu.end_date, 'id': edu.id})
    
    EducationFormSet = formset_factory(EducationForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        education_formset = EducationFormSet(request.POST)
        for form in education_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            
        
            if sections.index('education') == sections_len:
                print('the list is not end')
                section = sections[sections.index('education') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
            
            else:
                print('the list is end')
                return HttpResponseRedirect(reverse('cv:my-cvs'))

    else:
        education_formset = EducationFormSet(initial=objs)

    return render(request,'cv-forms/cv_education.html',{'education_formset':education_formset, 'user':user, 'cv': cv})


########## Certification
@login_required
def certifications(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    sections_len = len(sections)-1

    objs = []
    for cer in Certification.objects.filter(cv=cv):
        objs.append({'cv': cer.cv, 'name': cer.name, 'provider': cer.provider, 'date_obtained': cer.date_obtained, 'city': cer.city, 'id': cer.id})
    
    CertificationFormSet = formset_factory(CertificationForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        certification_formset = CertificationFormSet(request.POST)
        for form in certification_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            
        
            if sections.index('certifications') == sections_len:
                #print('the list is not end')
                section = sections[sections.index('sertifications') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
            
            else:
                #print('the list is end')
                return HttpResponseRedirect(reverse('cv:my-cvs'))

    else:
        certification_formset = CertificationFormSet(initial=objs)

    return render(request,'cv-forms/cv_certifications.html',{'certification_formset':certification_formset, 'user':user, 'cv': cv})



@login_required()
def my_cvs(request):
    user = request.user
    cvs = Cv.objects.filter(user=user).order_by('-created_at')
    return render(request, 'my_cvs.html', {'cvs': cvs})



@login_required()
def delete_cv(request, pk):
    cv = Cv.objects.get(pk=pk)
    cv.delete()
    messages.success(request, "Your Cv has been deleted!")
    return HttpResponseRedirect(reverse('cv:my-cvs'))



@login_required()
def cv_preview(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    return render(request,'cv-templates/%s.html' % cv.template, {'user':user, 'cv':cv})

@login_required()
def cv_view(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    return render(request,'cv/%s.html' % cv.template, {'user':user, 'cv':cv})

@login_required()
def change_template(request, pk):
    user = request.user
    resume = Resume.objects.get(pk=pk)
    form = ChooseForm(request.POST)
    if request.method == 'GET':
        form = ChooseForm()
    elif request.method == 'POST':
        if form.is_valid() and form.cleaned_data['resume_template'] == 'jakarta':
            resume.template = 'jakarta'
            
            resume.save()
            return render(request, 'resumes/jakarta.html', {'form': form, 'resume': resume})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'new_york':
            resume.template = 'new_york'
            
            resume.save()
            return render(request, 'resumes/new_york.html', {'form': form, 'resume': resume})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'tokyo':
            resume.template = 'tokyo'
            
            resume.save()
            return render(request, 'resumes/tokyo.html', {'form': form, 'resume': resume})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'rome':
            resume.template = 'rome'
            
            resume.save()
            return render(request, 'resumes/rome.html', {'form': form, 'resume': resume})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'san_francisco':
            resume.template = 'san_francisco'
            
            resume.save()
            return render(request, 'resumes/san_francisco.html', {'form': form, 'resume': resume})
    
    return render(request, 'resumes/template-choice.html', {'form': form, 'resume': resume})


@login_required()
def resume_pdf(request,pk):
    resume = Resume.objects.get(pk=pk)
    client = pdfcrowd.HtmlToPdfClient('bluesman20', '5d7e6ca5d0171d527f0cd5a76eb2341a')
    client.setUsePrintMedia(True)
    client.setPageHeight('-1')
    client.setDebugLog(True)
    # set HTTP response headers
    pdf_response = HttpResponse(content_type='application/pdf')
    pdf_response['Cache-Control'] = 'max-age=0'
    pdf_response['Accept-Ranges'] = 'none'
    content_disp = 'attachment' if 'asAttachment' in request.POST else 'inline'
 
    name = slugify(resume.name, allow_unicode=True)
    filename = "Resume_%s.pdf" %(name)
 
    pdf_response['Content-Disposition'] = content_disp + '; filename=My_resume.pdf'
  
    html = render_to_string('resumes/%s.html' % resume.template, {'resume': resume})
    client.convertStringToStream(html, pdf_response)
    # send the generated PDF
    return pdf_response

    


'''
###############
def work_experience(request, pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    work_experience = WorkExperience.objects.filter(cv=cv)
    sections = cv.sections
    form = WorkExperienceForm(instance=cv)
    WorkExperienceFormSet = modelformset_factory(WorkExperience, form=form, formset=MyModelFormSet, extra=1, max_num=10)
    
    #print(sections[sections.index('education') + 1])
    if request.method == 'POST':
        formset= WorkExperienceFormSet(request.POST or None)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                position = form.cleaned_data.get("position")
                company = form.cleaned_data.get("company")
                country = form.cleaned_data.get("country")
                city = form.cleaned_data.get("city")
                start_date = form.cleaned_data.get("start_date")
                end_date = form.cleaned_data.get("end_date")
                achievements = form.cleaned_data.get("achievements")

                #form.save(commit=False)

                work_experience = WorkExperience()
                work_experience.position = position
                work_experience.company = company
                work_experience.country = country
                work_experience.city = city
                work_experience.start_date = start_date
                work_experience.end_date = end_date
                work_experience.achievements = achievements
                work_experience.cv = cv
                #work_experience = WorkExperience.objects.create(cv=cv, company = company, position = position,country = country, city=city, start_date=start_date, end_date=end_date, achievements=achievements)
                work_experience.save()
                #print(position,'has been saved!')

        #section = sections[sections.index('work_experience') + 1]
        #return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':cv.pk}))
    else:   
        formset = WorkExperienceFormSet()
    
    return render(request,'cv-forms/cv_experience.html',{'formset':formset,'user':user, 'cv': cv, 'work_experience':work_experience})


def education(request, pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    educations = Education.objects.filter(cv=cv)
    sections = cv.sections
    forms = EducationFormSet()  
    #print(sections[sections.index('education') + 1])

    if request.method == 'POST':
        formset= EducationFormSet(request.POST or None)
        for form in formset:
            if form.is_valid():
                
                school = form.cleaned_data.get("school")
                department = form.cleaned_data.get("department")
                major = form.cleaned_data.get("major")
                degree = form.cleaned_data.get("degree")
                country = form.cleaned_data.get("country")
                city = form.cleaned_data.get("city")
                start_date = form.cleaned_data.get("start_date")
                end_date = form.cleaned_data.get("end_date")
                description = form.cleaned_data.get("description")
                form.save(commit=False)
                education = Education()
                education.school = school
                education.department = department
                education.major = major
                education.degree = degree
                education.country = country
                education.city = city
                education.start_date = start_date
                education.end_date = end_date
                education.description = description
                education.cv = cv
                education.save()



    return render(request,'cv-forms/cv_education.html',{'forms':forms, 'user':user, 'cv': cv,'educations':educations})

'''