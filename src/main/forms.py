from django import forms
from django.conf import settings
from django.forms import ModelForm, TextInput, NumberInput, DateInput, DateField
from django.forms import BaseModelFormSet
from django.forms import modelformset_factory
from django.forms.formsets import formset_factory
from users.models import Profile
from .models import Certification, Education, CustomSection, Language, Cv, Skill, WorkExperience, Project, Course, Publication, Hobby
from tinymce.widgets import TinyMCE
from .choices import CV_CHOICES


class ChooseForm(forms.Form):
    cv_template = forms.ChoiceField(choices=CV_CHOICES, required=True)

    '''
    def clean_resume_template(self):
        data = self.cleaned_data['resume_template']
        if not data:
            raise forms.ValidationError('Please select a resume!')
        return data
    '''

    class Meta:
        pass


# allows validation on empty forms for ResumeWizard
class MyModelFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(MyModelFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class CvForm(ModelForm):
    template = forms.ChoiceField(choices=CV_CHOICES, required=True)
    class Meta:
        model = Cv
        fields = ['name', 'user', 'id', 'sections','template']
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'For example: Data Scientist or Manager..'}),
                   'template': forms.CheckboxInput(),
                   'user': forms.HiddenInput(),
                   'id': forms.HiddenInput(), }
                   
        labels = {'name': 'Cv name'}


class WorkExperienceForm(ModelForm):
    id = forms.CharField(label='Id', max_length=100, required=False)
    start_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    end_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                         widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    
    class Meta:
        model = WorkExperience
        fields = ['position', 'company', 'city', 'start_date', 'end_date', 'achievements', 'cv', 'id']
        widgets = {'achievements': TinyMCE(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}),
                   'position': TextInput(attrs={'placeholder': 'For example: Bank Teller'}),
                   'company': TextInput(attrs={'placeholder': 'For example: Bank Central Eurpe'}),
                   'city': TextInput(attrs={'placeholder': 'For example: Jakarta'}),
                   #'cv': forms.HiddenInput(),
                   'id': forms.HiddenInput(),
                   }
        labels = {'achievements': 'Description'}

    def save(self, commit=False, *args, **kwargs):
        m = super(WorkExperienceForm, self).save(commit=False, *args, **kwargs)

        if not self.cleaned_data['id']:
            ex = WorkExperience()
        else:
            ex = WorkExperience.objects.get(pk=m.self.cleaned_data['id'])

        ex.position = m.position
        ex.achievements = m.achievements
        ex.city = m.city
        ex.company = m.company
        ex.start_date = m.start_date
        ex.end_date = m.end_date
        ex.cv = m.cv
        ex.save()

    """ def as_myp(self):
        "Return this form rendered as HTML <p>s."
        return self._html_output(
            normal_row='<p%(html_class_attr)s class="%(label)s">%(label)s %(field)s%(help_text)s</p>',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True,
        ) """

    
#WorkExperienceFormSet = modelformset_factory(WorkExperience, form=WorkExperienceForm, formset=MyModelFormSet, extra=1, max_num=10)


class CertificationForm(ModelForm):
    date_obtained = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                              widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))

    class Meta:
        model = Certification
        fields = ['name', 'provider', 'date_obtained', 'city', 'cv', ]
        widgets = {'name': TextInput(attrs={'placeholder': 'For example: Certified Technical Architect'}),
                    'provider': TextInput(attrs={'placeholder': 'For example: Coursera, LinkedIn...'}),
                   'city': TextInput(attrs={'placeholder': 'For example: New York'}),
                   'cv': forms.HiddenInput(), }
        labels = {'name': 'Certification', 'provider': 'Provider', 'date_obtained': 'When'}

    def save(self, commit=False, *args, **kwargs):
        m = super(CertificationForm, self).save(commit=False, *args, **kwargs)

        if not m.id:
            cer = Certification()
        else:
            cer = Certification.objects.get(pk=m.id)

        cer.name = m.name
        cer.provider = m.provider
        cer.date_obtained = m.date_obtained
        cer.city = m.city
        cer.cv = m.cv
        cer.save()

#CertificationFormSet = modelformset_factory(Certification, form=CertificationForm, formset=MyModelFormSet, max_num=15)


class EducationForm(ModelForm):
    id = forms.CharField(label='Id', max_length=100, required=False)
    start_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    end_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                         widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))

    class Meta:
        model = Education
        fields = ['school', 'department','degree', 'major', 'country', 'city', 'start_date', 'end_date', 'description', 'cv', 'id' ]
        widgets = {'school': TextInput(attrs={'placeholder': 'For example: University of San Francisco'}),
                    'department': TextInput(attrs={'placeholder': 'For example: Computer Science'}),
                   'degree': TextInput(attrs={'placeholder': 'For example: Bachelor of Science'}),
                   'major': TextInput(attrs={'placeholder': 'For example: Economics'}),
                   'city': TextInput(attrs={'placeholder': 'For example: San Francisco'}),
                   'description': TinyMCE(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}),
                   #'cv': forms.HiddenInput(),
                    }
        labels = {'school': 'Institution', 'major':'Speciality' }

    def save(self, commit=False, *args, **kwargs):
        m = super(EducationForm, self).save(commit=False, *args, **kwargs)

        if not self.cleaned_data['id']:
            ed = Education()
        else:
            ed = Education.objects.get(pk=self.cleaned_data['id'])

        ed.school = m.school
        ed.department = m.department
        ed.degree = m.degree
        ed.major = m.major
        ed.city = m.city
        ed.description = m.description
        ed.start_date = m.start_date
        ed.end_date = m.end_date
        ed.cv = m.cv
        ed.save()

#EducationFormSet = modelformset_factory(Education, form=EducationForm, formset=MyModelFormSet, max_num=10)


class SkillForm(ModelForm):
    def clean(self):
        cleaned_data = super(SkillForm, self).clean()
        name = cleaned_data.get('name')
        competency = cleaned_data.get('competency')

        if name and competency not in [1, 2, 3, 4, 5]:
                raise forms.ValidationError("Please select a competency level for your skill")

        if competency in [1, 2, 3, 4, 5] and not name:
                raise forms.ValidationError("Please enter a skill first")

    class Meta:
        model = Skill
        fields = ['name', 'competency', 'cv', ]
        widgets = {'competency': forms.Select(attrs={'class': 'form-control'}),
                   'name': TextInput(attrs={'placeholder': 'For example: Microsoft Excel'}),
                   'cv': forms.HiddenInput(), }
        labels = {'name': 'Skill', 'competency': 'Level'}
    
    def save(self, commit=False, *args, **kwargs):
        m = super(SkillForm, self).save(commit=False, *args, **kwargs)

        if not m.id:
            ski = Skill()
        else:
            ski = Skill.objects.get(pk=m.id)

        ski.name = m.name
        ski.competency = m.competency
        ski.cv = m.cv
        ski.save()

#SkillFormSet = modelformset_factory(Skill, form=SkillForm, formset=MyModelFormSet, max_num=15)


class LanguageForm(ModelForm):
    def clean(self):
        cleaned_data = super(LanguageForm, self).clean()
        name = cleaned_data.get('name')
        competency = cleaned_data.get('competency')

        if name and competency not in [1, 2, 3, 4, 5]:
                raise forms.ValidationError("Please select a competency level for your language")

        if competency in [1, 2, 3, 4, 5] and not name:
                raise forms.ValidationError("Please enter a language first")

    class Meta:
        model = Language
        fields = ['name', 'competency','read','write','speak', 'cv', ]
        widgets = {'competency': forms.Select(attrs={'class': 'form-control'}),
                   'name': TextInput(attrs={'placeholder': 'For example: English or Russian'}),
                   #'read':forms.CheckboxInput,
                   #'write':forms.CheckboxInput,
                   #'speak':forms.CheckboxInput,
                   'cv': forms.HiddenInput(), }
        labels = {'name': 'Language', 'competency': 'Level'}
    
    def save(self, commit=False, *args, **kwargs):
        m = super(LanguageForm, self).save(commit=False, *args, **kwargs)

        if not m.id:
            lang = Language()
        else:
            cer = Language.objects.get(pk=m.id)

        lang.name = m.name
        lang.competency = m.competency
        lang.read = m.read
        lang.write = m.write
        lang.speak = m.speak
        lang.cv = m.cv
        lang.save()

#LanguageFormSet = modelformset_factory(Language, form=LanguageForm, formset=MyModelFormSet, max_num=15)


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['job_title', 'address', 'address2', 'city', 'country', 'phone_number', 'linked_in', 'objective',
                  'profile_pic', ]
        widgets = {'job_title': TextInput(attrs={'placeholder': 'What is your desired job title?'}),
                   'address': TextInput(attrs={'placeholder': 'What is your home street address?'}),
                   'address2': TextInput(attrs={'placeholder': 'Neighborhood or sub-district'}),
                   'city': TextInput(attrs={'placeholder': 'What city do you live in?'}),
                   'phone_number': TextInput(attrs={'placeholder': 'What is your mobile number?', }),
                   'linked_in': TextInput(attrs={'placeholder': 'What is your LinkedIn profile?'}), }
        labels = {"linked_in": "LinkedIn profile",
                  "phone_number": "Mobile",
                  "profile_pic": "Profile picture",
                  "objective": "About Me",
                  "address2": "Address", }

class ProjectForm(ModelForm):
    start_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    end_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                         widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))

    class Meta:
        model = Project
        fields = [
            'name',
            'start_date',
            'end_date',
            'role',
            'description',
            'cv',
            ]
        widgets = {'cv': forms.HiddenInput(),}
        labels = {'name': 'Project'}
    
    def save(self, commit=False, *args, **kwargs):
        m = super(ProjectForm, self).save(commit=False, *args, **kwargs)

        if not self.cleaned_data['id']:
            pro = Project()
        else:
            pro = Project.objects.get(pk=self.cleaned_data['id'])

        pro.name = m.name
        pro.role = m.role
        pro.description = m.description
        pro.start_date = m.start_date
        pro.end_date = m.end_date
        pro.cv = m.cv
        pro.save()

#ProjectFormSet = modelformset_factory(Project, form=ProjectForm, formset=MyModelFormSet, max_num=10)


class PublicationForm(ModelForm):
    publication_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    
    class Meta:
        model = Publication
        fields = [
            'title',
            'publisher',
            'publication_date',
            'publication_url',
            'description',
            'cv',
            ]
        widgets = {'cv': forms.HiddenInput(),}
        labels = {'name': 'Publication'}
    
    def save(self, commit=False, *args, **kwargs):
        m = super(PublicationForm, self).save(commit=False, *args, **kwargs)

        if not self.cleaned_data['id']:
            pub = Publication()
        else:
            pub = Publication.objects.get(pk=self.cleaned_data['id'])

        pub.title = m.title
        pub.publisher = m.publisher
        pub.publication_date = m.publication_date
        pub.publication_url = m.publication_url
        pub.description = m.description
        pub.cv = m.cv
        pub.save()

#PublicationFormSet = modelformset_factory(Publication, form=PublicationForm, formset=MyModelFormSet, max_num=10)


class CourseForm(ModelForm):
    id = forms.CharField(label='Id', max_length=100, required=False)
    start_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    end_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    class Meta:
        model = Course
        fields = [
            'course_name',
            'school',
            'major',
            'start_date',
            'end_date',
            'country',
            'description',
            'online_course',
            'cv',
            ]
        widgets = {'cv': forms.HiddenInput(),}
        labels = {'course_name': 'Course'}

    def save(self, commit=False, *args, **kwargs):
        m = super(CourseForm, self).save(commit=False, *args, **kwargs)

        if not self.cleaned_data['id']:
            cour = Course()
        else:
            cour = Course.objects.get(pk=self.cleaned_data['id'])

        cour.course_name = m.course_name
        cour.school = m.school
        cour.major = m.major
        cour.start_date = m.start_date
        cour.end_date = m.end_date
        cour.country = m.country
        cour.description = m.description
        cour.online_course = m.online_course
        cour.cv = m.cv
        cour.save()
        
#CourseFormSet = modelformset_factory(Course, form=CourseForm, formset=MyModelFormSet, max_num=10)


class HobbyForm(ModelForm):
    
    class Meta:
        model = Hobby
        fields = [
            'name',
            'cv',
            ]
        widgets = {'cv': forms.HiddenInput(),}
        labels = {'name': 'Hobby'}

    def save(self, commit=False, *args, **kwargs):
        m = super(HobbyForm, self).save(commit=False, *args, **kwargs)

        if not self.cleaned_data['id']:
            hob = Hobby()
        else:
            hob = CustomSection.objects.get(pk=self.cleaned_data['id'])

        hob.name = m.name       
        hob.cv = m.cv
        hob.save()

#HobbyFormSet = modelformset_factory(Hobby, form=HobbyForm, formset=MyModelFormSet, max_num=10)


class CustomForm(ModelForm):
    
    class Meta:
        model = CustomSection
        fields = [
            'title',
            'subtitle',
            'description',
            'cv',
            ]
        widgets = {'cv': forms.HiddenInput(),}
        labels = {'title': 'Custom Section'}

    def save(self, commit=False, *args, **kwargs):
        m = super(CustomForm, self).save(commit=False, *args, **kwargs)

        if not self.cleaned_data['id']:
            cs = CustomSection()
        else:
            cs = CustomSection.objects.get(pk=self.cleaned_data['id'])

        cs.title = m.title
        cs.subtitle = m.subtitle
        cs.description = m.description
        cs.cv = m.cv
        cs.save()

#CustomFormSet = modelformset_factory(CustomSection, form=CustomForm, formset=MyModelFormSet, max_num=10)



class TemplateChoiceForm(forms.Form):
    template = forms.ChoiceField(choices=CV_CHOICES, required=True)
    class Meta:
        model = Cv
        fields = ['template', ]

