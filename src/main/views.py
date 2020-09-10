import logging
from django.contrib.auth.models import Group
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
#from formtools.wizard.views import SessionWizardView
from django_slugify_processor.text import slugify
from users.forms import CustomUserChangeForm
from .forms import *
from .models import *
import pdfcrowd
import ssl
from django.shortcuts import redirect

ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################# Simple Cv Builder ###########################

####### Create CV #######
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

####### Experience #######
@login_required
def work_experience(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    objs = []
    for exp in WorkExperience.objects.filter(cv=cv):
        objs.append({'cv': exp.cv, 'position': exp.position, 'company': exp.company, 'achievements': exp.achievements, 'city': exp.city, 'start_date': exp.start_date, 'end_date': exp.end_date, 'id': exp.id})
    WorkExperienceFormSet = formset_factory(WorkExperienceForm, extra=4)
    objs.append({'cv': cv})

    
    if request.method == 'POST':
        experience_formset = WorkExperienceFormSet(request.POST)
        for form in experience_formset:
            
            print('Loop formset')
            if form.is_valid():
                
                form.save()
            section = sections[sections.index('work_experience') + 1]
            return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))       
    
    else:
        experience_formset = WorkExperienceFormSet(initial=objs)

    return render(request,'cv-forms/cv_experience.html',{'experience_formset':experience_formset, 'user':user, 'cv': cv})

####### Education #######
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
                return HttpResponseRedirect(reverse('cv:cv_done', kwargs={'pk':pk}))
            else:
                print('the list is end')
                section = sections[sections.index('education') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
                

    else:
        education_formset = EducationFormSet(initial=objs)

    return render(request,'cv-forms/cv_education.html',{'education_formset':education_formset, 'user':user, 'cv': cv})

####### Certifications #######
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
                return HttpResponseRedirect(reverse('cv:cv_done', kwargs={'pk':pk}))

                
            else:
                section = sections[sections.index('certifications') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
            

    else:
        certification_formset = CertificationFormSet(initial=objs)

    return render(request,'cv-forms/cv_certifications.html',{'certification_formset':certification_formset, 'user':user, 'cv': cv})

####### Courses #######
@login_required
def courses(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    sections_len = len(sections)-1

    objs = []
    for sec in Course.objects.filter(cv=cv):
        objs.append({'cv': cour.cv, 'course_name': cour.course_name, 'school': cour.school, 'major': cour.major, 'start_date': cour.start_date, 'end_date': cour.end_date, 'country': cour.country, 'description': cour.description, 'online_course': cour.online_course, 'id': cour.id})
    
    CourseFormSet = formset_factory(CourseForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        courses_formset = CourseFormSet(request.POST)
        for form in courses_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            
        
            if sections.index('courses') == sections_len:
                print('the list is not end')
                return HttpResponseRedirect(reverse('cv:cv_done', kwargs={'pk':pk}))
            else:
                print('the list is end')
                section = sections[sections.index('courses') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
                

    else:
        courses_formset = CourseFormSet(initial=objs)

    return render(request,'cv-forms/cv_courses.html',{'courses_formset':courses_formset, 'user':user, 'cv': cv})

####### Projects #######
@login_required
def projects(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    sections_len = len(sections)-1

    objs = []
    for pro in Project.objects.filter(cv=cv):
        objs.append({'cv': pro.cv, 'name': pro.name, 'role': pro.role, 'start_date': pro.start_date, 'end_date': pro.end_date, 'description': pro.description, 'id': pro.id})
    
    ProjectFormSet = formset_factory(ProjectForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        projects_formset = ProjectFormSet(request.POST)
        for form in projects_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            
        
            if sections.index('projects') == sections_len:
                print('the list is not end')
                return HttpResponseRedirect(reverse('cv:cv_done', kwargs={'pk':pk}))
            else:
                print('the list is end')
                section = sections[sections.index('projects') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
                

    else:
        projects_formset = ProjectFormSet(initial=objs)

    return render(request,'cv-forms/cv_projects.html',{'projects_formset':projects_formset, 'user':user, 'cv': cv})

####### Skills #######
@login_required
def skills(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    sections_len = len(sections)-1

    objs = []
    for ski in Skill.objects.filter(cv=cv):
        objs.append({'cv': ski.cv, 'name': ski.name, 'competency': ski.competency, 'id': ski.id})
    
    SkillFormSet = formset_factory(SkillForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        skills_formset = SkillFormSet(request.POST)
        for form in skills_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            
        
            if sections.index('skills') == sections_len:
                print('the list is not end')
                return HttpResponseRedirect(reverse('cv:cv_done', kwargs={'pk':pk}))
            else:
                print('the list is end')
                section = sections[sections.index('skills') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
                

    else:
        skills_formset = SkillFormSet(initial=objs)

    return render(request,'cv-forms/cv_skills.html',{'skills_formset':skills_formset, 'user':user, 'cv': cv})

####### Languages #######
@login_required
def languages(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    sections_len = len(sections)-1

    objs = []
    for lang in Language.objects.filter(cv=cv):
        objs.append({'cv': lang.cv, 'name': lang.name, 'competency': lang.competency, 'read':lang.read,  'write':lang.write, 'speak':lang.speak, 'id': lang.id})
    
    LanguageFormSet = formset_factory(LanguageForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        languages_formset = LanguageFormSet(request.POST)
        for form in languages_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            
        
            if sections.index('languages') == sections_len:
                print('the list is not end')
                return HttpResponseRedirect(reverse('cv:cv_done', kwargs={'pk':pk}))
            else:
                print('the list is end')
                section = sections[sections.index('languages') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
                

    else:
        languages_formset = LanguageFormSet(initial=objs)

    return render(request,'cv-forms/cv_languages.html',{'languages_formset':languages_formset, 'user':user, 'cv': cv})

####### Publications #######
@login_required
def publications(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    sections_len = len(sections)-1

    objs = []
    for pub in Publication.objects.filter(cv=cv):
        objs.append({'cv': pub.cv, 'title': pub.title, 'publisher': pub.publisher, 'publication_date':pub.publication_date,  'publication_url':pub.publication_url, 'description':pub.description, 'id': pub.id})
    
    PublicationFormSet = formset_factory(PublicationForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        publications_formset = PublicationFormSet(request.POST)
        for form in publications_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            
        
            if sections.index('publications') == sections_len:
                print('the list is not end')
                return HttpResponseRedirect(reverse('cv:cv_done', kwargs={'pk':pk}))
            else:
                print('the list is end')
                section = sections[sections.index('publications') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
                

    else:
        publications_formset = PublicationFormSet(initial=objs)

    return render(request,'cv-forms/cv_publications.html',{'publications_formset':publications_formset, 'user':user, 'cv': cv})

####### custom_section #######
@login_required
def custom_section(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    sections_len = len(sections)-1

    objs = []
    for cs in CustomSection.objects.filter(cv=cv):
        objs.append({'cv': cs.cv, 'title': cs.title, 'subtitle': cs.subtitle, 'description': cs.description, 'id': cs.id})
    
    CustomFormSet = formset_factory(CustomForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        customforms_formset = CustomFormSet(request.POST)
        for form in customforms_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            
        
            if sections.index('custom_section') == sections_len:
                print('the list is not end')
                return HttpResponseRedirect(reverse('cv:cv_done', kwargs={'pk':pk}))
            else:
                print('the list is end')
                section = sections[sections.index('custom_section') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
                

    else:
        customforms_formset = CustomFormSet(initial=objs)

    return render(request,'cv-forms/cv_custom_sections.html',{'custom_section':custom_section, 'user':user, 'cv': cv})

####### hobbies #######
@login_required
def hobbies(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    sections = cv.sections
    sections_len = len(sections)-1

    objs = []
    for hob in Hobby.objects.filter(cv=cv):
        objs.append({'cv': hob.cv, 'name': hob.name, 'id': hob.id})
    
    HobbyFormSet = formset_factory(HobbyForm, extra=1)
    objs.append({'cv': cv})
    
    if request.method == 'POST':
        hobbies_formset = HobbyFormSet(request.POST)
        for form in hobbies_formset:
            print('Loop formset')
            if form.is_valid():
                form.cv = pk
                form.save()
            
        
            if sections.index('hobbies') == sections_len:
                print('the list is not end')
                return HttpResponseRedirect(reverse('cv:cv_done', kwargs={'pk':pk}))
            else:
                print('the list is end')
                section = sections[sections.index('hobbies') + 1]
                return HttpResponseRedirect(reverse('cv:%s' % section, kwargs={'pk':pk}))
                

    else:
        hobbies_formset = HobbyFormSet(initial=objs)

    return render(request,'cv-forms/cv_hobbies.html',{'hobbies_formset':hobbies_formset, 'user':user, 'cv': cv})



    user = request.user
    cv = Cv.objects.get(pk=pk)
    form = CvForm(instance=cv)  
    experience = WorkExperienceFormSet()
    education = EducationFormSet()
    languages = LanguageFormSet()
    skills = SkillFormSet()


    if request.method == 'POST':
        experience = WorkExperienceFormSet(request.POST, request.FILES, instance=cv)
        if experience.is_valid():
            experience.save()
        else:
            experience = WorkExperienceFormSet(instance=cv)

    ### Education  ###
    if request.method == 'POST':
        education = EducationFormSet(request.POST, request.FILES, instance=cv)
        if education.is_valid():
            education.save()
        else:
            education = EducationFormSet(instance=cv)
    
    ### Languages  ###
    
    if request.method == 'POST':
        languages = LanguageFormSet(request.POST, request.FILES, instance=cv)
        if languages.is_valid():
            languages.save()
        else:
            languages = LanguageFormSet(instance=cv)

    ### Skills  ###
    if request.method == 'POST':
        skills = SkillFormSet(request.POST, request.FILES, instance=cv)
        if skills.is_valid():
            skills.save()
        else:
            skills = SkillFormSet(instance=cv)
    

    context = {
        'cv': cv,
        'education': education,
        'experience': experience,
        'languages': languages,
        'skills': skills, 
        'user':user,
        

    }
    return render(request,'cv_data.html', context)

####### Done Page #######
@login_required()
def cv_done(request,pk):
    user = request.user
    cv = Cv.objects.get(pk=pk)
    return render(request,'cv-forms/cv_done.html', {'user':user, 'cv':cv})


################################# Wizard Cv Builder #######################
"""
from .wizardform import WorkExperienceFormset

FORMS = [('cvs', CvForm),
         ('work_experience', WorkExperienceFormset),
         ('education', EducationFormset),
         ('certifications', CertificationFormSet),
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
""" 

@login_required()
def choose(request, pk):
    user = request.user
    pp_url = user.profile.profile_pic.url.strip('/')
    resume = Resume.objects.get(pk=pk)
    form = ChooseForm(request.POST)
    group = Group.objects.get(name='paying_user')
    if request.method == 'GET':
        form = ChooseForm()
    elif request.method == 'POST' and 'view-resume' in request.POST:
        if form.is_valid() and form.cleaned_data['resume_template'] == 'jakarta':
            return render(request, 'resumes/jakarta.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'new_york':
            return render(request, 'resumes/new_york.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'tokyo':
            return render(request, 'resumes/tokyo.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'rome':
            return render(request, 'resumes/rome.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'sf':
            return render(request, 'resumes/san_francisco.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
    # two buttons on one page
    elif form.is_valid() and request.method == 'POST' and 'export-resume' in request.POST:
        if request.user.groups.filter(name='paying_user').exists():
            # code for exporting pdfcrowd goes here
            client = pdfcrowd.HtmlToPdfClient('chrisgunawan85', 'ea5734a7dc5aabbded5e65d8a32de8a4')
            client.setUsePrintMedia(True)
            client.setPageHeight('-1')
            client.setDebugLog(True)
            # set HTTP response headers
            pdf_response = HttpResponse(content_type='application/pdf')
            pdf_response['Cache-Control'] = 'max-age=0'
            pdf_response['Accept-Ranges'] = 'none'
            content_disp = 'attachment' if 'asAttachment' in request.POST else 'inline'
            pdf_response['Content-Disposition'] = content_disp + '; filename=my_resume.pdf'

            if form.cleaned_data['resume_template'] == 'jakarta':
                html = render_to_string('resumes/jakarta.html', {'resume': resume, 'pp_url': pp_url})
            if form.cleaned_data['resume_template'] == 'new_york':
                html = render_to_string('resumes/new_york.html', {'resume': resume, 'pp_url': pp_url})
            if form.cleaned_data['resume_template'] == 'tokyo':
                html = render_to_string('resumes/tokyo.html', {'resume': resume, 'pp_url': pp_url})
            if form.cleaned_data['resume_template'] == 'rome':
                html = render_to_string('resumes/rome.html', {'resume': resume, 'pp_url': pp_url})
            if form.cleaned_data['resume_template'] == 'sf':
                html = render_to_string('resumes/san_francisco.html', {'resume': resume, 'pp_url': pp_url})

            client.convertStringToStream(html, pdf_response)
            # send the generated PDF
            return pdf_response
        else:
            messages.info(request, "Please purchase a package to export to PDF format")
            return HttpResponseRedirect(reverse('resumes:payment'))
    return render(request, 'resumes/choose.html', {'form': form, 'resume': resume})

@login_required()
def my_cvs(request):
    user = request.user
    cvs = Cv.objects.filter(user=user).order_by('-created_at')
    return render(request, 'my_cvs.html', {'cvs': cvs})

@login_required()
def templates(request):
    return render(request, 'cv/templates.html')

@login_required()
def delete_cv(request, pk):
    cv = Cv.objects.get(pk=pk)
    cv.delete()
    messages.success(request, "Your Cv has been deleted!")
    return HttpResponseRedirect(reverse('cv:my-cvs'))

def dict_has_data(input_dict):
    has_data = False
    
    for key in input_dict:
        if input_dict[key]:
            has_data = True
            break
    #print(input_dict)
    return has_data
'''
class CvWizard(LoginRequiredMixin, SessionWizardView):
    login_url = '/login/'

    def get_form_initial(self, step):
        if 'pk' in self.kwargs:
            return {}
        return self.initial_dict.get(step, {})

    def get_form_instance(self, step):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            cv = Cv.objects.get(id=pk)
            sections = cv.sections
            print(sections)
            
            if step == 'cvs':
                return cv

            if step == 'work_experience':
                return cv.workexperience_set.all()

            if step == 'education':
                return cv.education_set.all()

            if step == 'certifications':
                return cv.certification_set.all()
                    
            if step == 'projects':
                return cv.project_set.all()

            if step == 'skills':
                return cv.skill_set.all()

            if step == 'languages':
                return cv.language_set.all()
            ### mix multiple forms in one step (education, experience....)
            ### forms from list of section chosen by user in the first step

            
            
        else:
            if step == 'cvs':
                return None
            
            ### mix multiple forms in one step (education, experience....)
        
            if step == 'work_experience':
                return WorkExperience.objects.none()

            if step == 'education':
                return Education.objects.none()

            if step == 'certifications':
                return Certification.objects.none()

            if step == 'projects':
                return Project.objects.none()

            if step == 'skills':
                return Skill.objects.none()

            if step == 'languages':
                return Language.objects.none()
                
        return None

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        user = self.request.user
        cv_form_data = self.get_cleaned_data_for_step('cvs')
        cv_name = cv_form_data['name']
        cv_sections = cv_form_data['sections']
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = None
        cv, created = Cv.objects.update_or_create(id=pk, defaults={'user': user,'name': cv_name, 'sections':cv_sections })

        for form_name in FORM_TYPES:
            form_data_list = self.get_cleaned_data_for_step(form_name)
            for form_data in form_data_list:
                if not dict_has_data(form_data):
                    continue
                form_data['cv'] = cv

                form_instance = self.get_form(step=form_name)
                obj = form_data.pop('id')
                if obj:
                    form_instance.model.objects.filter(id=obj.id).update(**form_data)
                else:
                    form_instance.model.objects.create(**form_data)

        messages.add_message(self.request, messages.SUCCESS, 'Your cv has been saved!')
        return HttpResponseRedirect(reverse('cv:my-cvs'))
'''
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





#### PDF Generating & Downloading ####
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

from django.http import HttpResponse
from django.views.generic import View
#from resumes.utils import render_to_pdf #created in step 4
#from io import BytesIO
#from django.http import HttpResponse
#from django.template.loader import get_template
#from xhtml2pdf import pisa
""" 
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

 """
'''
@login_required()
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        resume = Resume.objects.get(pk=pk)
        pdf = render_to_pdf('resumes/%s.html' % resume.template, {'resume': resume})
        return HttpResponse(pdf, content_type='application/pdf')



class GeneratePdf(View):

    def get(self, request, *args, **kwargs):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            resume = Resume.objects.get(id=pk)
        template = get_template('resumes/%s.html' % resume.template)
        html = template.render({'resume': resume})
        pdf = render_to_pdf('resumes/%s.html' % resume.template, {'resume': resume})
        response = HttpResponse(pdf, content_type='application/pdf')
        name = slugify(resume.name, allow_unicode=True)

        filename = "Resume_%s.pdf" %(name)
        content = "inline; filename='%s'" %(filename)
        
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
        return HttpResponse("Not found")


class ViewPdf(View):

    def get(self, request, *args, **kwargs):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            resume = Resume.objects.get(id=pk)
        
        pdf = render_to_pdf('resumes/%s.html' % resume.template, {'resume': resume})
        return HttpResponse(pdf, content_type='application/pdf')

def resume_view_pdf(View,pk):
    def get(self, request, *args, **kwargs):
        resume = Resume.objects.get(pk=pk)
        pdf = render_to_pdf('resumes/%s.html' %resume.template, {'resume': resume})
        return HttpResponse(pdf, content_type='application/pdf')

"""
if step == 'templates':
                template = resume.template
                form = TemplateChoiceForm(request.POST)
                resume = Resume.objects.get(id=pk)
                if request.method == 'POST':
                    form = TemplateChoiceForm(request.POST, request.FILES, instance=resume)        
                    if form.is_valid() and form.cleaned_data['resume_template'] == 'jakarta':
                        resume.template = 'jakarta'
                        form.save()
                        resume.save()
                    if form.is_valid() and form.cleaned_data['resume_template'] == 'new_york':
                        resume.template = 'new_york'
                        form.save()
                        resume.save()
                    if form.is_valid() and form.cleaned_data['resume_template'] == 'tokyo':
                        resume.template = 'tokyo'
                        form.save()
                        resume.save()
                    if form.is_valid() and form.cleaned_data['resume_template'] == 'rome':
                        resume.template = 'rome'
                        form.save()
                        resume.save()
                    if form.is_valid() and form.cleaned_data['resume_template'] == 'sf':
                        resume.template = 'san_francisco'          
                        template.save() 
                        resume.save()  
                        
                else:
                    form = TemplateChoiceForm(instance=resume)  
                return form  
"""

""" from easy_pdf.views import PDFTemplateView

class easyPdfView(PDFTemplateView):
    template_name = 'hello.html'


    def get(self, request, *args, **kwargs):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            resume = Resume.objects.get(id=pk)
        template = get_template('resumes/%s.html' % resume.template)
        html = template.render({'resume': resume})
        pdf = render_to_pdf('resumes/%s.html' % resume.template, {'resume': resume})
        response = HttpResponse(pdf, content_type='application/pdf')
        name = slugify(resume.name, allow_unicode=True)

        filename = "Resume_%s.pdf" %(name)
        content = "inline; filename='%s'" %(filename)
        
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
        return HttpResponse("Not found") """


from wkhtmltopdf.views import PDFTemplateView

class MyPDF(PDFTemplateView):

    def get(self, request, *args, **kwargs):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            resume = Resume.objects.get(id=pk)
    
            template = 'resumes/%s.html' % resume.template
            name = slugify(resume.name, allow_unicode=True)
            filename = "Resume_%s.pdf" %(name)
            
            cmd_options = {
                'margin-top': 3,
            }

            return HttpResponse(resume, content_type='application/pdf')


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def pdf_download(request, pk):
    # Create a file-like buffer to receive PDF data.
    resume = Resume.objects.get(pk=pk)
    template = 'resumes/%s.html' % resume.template


    name = slugify(resume.name, allow_unicode=True)
    filename = "Resume_%s.pdf" %(name)
        
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, template)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=filename)


import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa 


def generate_PDF(request,pk):
    resume = Resume.objects.get(pk=pk)
    data = {'resume': resume}

    template = get_template('resumes/%s.html' % resume.template)
    html  = template.render(data)

    #file = open(html, "w+b")
    #pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=html,
          #  encoding='utf-8')

    """ file.seek(0)
    pdf = file.read()
    file.close()    """         
    return HttpResponse(html, 'application/pdf')

'''