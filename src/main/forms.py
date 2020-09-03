from django import forms
from django.conf import settings
from django.forms import ModelForm, TextInput, NumberInput, DateInput, DateField
from django.forms import BaseModelFormSet
from django.forms import modelformset_factory
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
    start_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    end_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                         widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    
    class Meta:
        model = WorkExperience
        fields = ['position', 'company', 'city', 'start_date', 'end_date', 'achievements', 'cv', ]
        widgets = {'achievements': TinyMCE(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}),
                   'position': TextInput(attrs={'placeholder': 'For example: Bank Teller'}),
                   'company': TextInput(attrs={'placeholder': 'For example: Bank Central Eurpe'}),
                   'city': TextInput(attrs={'placeholder': 'For example: Jakarta'}),
                   'cv': forms.HiddenInput(), }
        labels = {'achievements': 'Description'}

WorkExperienceFormSet = modelformset_factory(WorkExperience, form=WorkExperienceForm, formset=MyModelFormSet, extra=1,
                                             max_num=10)


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


CertificationFormSet = modelformset_factory(Certification, form=CertificationForm, formset=MyModelFormSet, max_num=15)


class EducationForm(ModelForm):
    start_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
    end_date = DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                         widget=DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))

    class Meta:
        model = Education
        fields = ['school', 'department','degree', 'major', 'country', 'city', 'start_date', 'end_date', 'description','cv', ]
        widgets = {'school': TextInput(attrs={'placeholder': 'For example: University of San Francisco'}),
                    'department': TextInput(attrs={'placeholder': 'For example: Computer Science'}),
                   'degree': TextInput(attrs={'placeholder': 'For example: Bachelor of Science'}),
                   'major': TextInput(attrs={'placeholder': 'For example: Economics'}),
                   'city': TextInput(attrs={'placeholder': 'For example: San Francisco'}),
                   'achievements': TinyMCE(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}),
                   'cv': forms.HiddenInput(), }
        labels = {'school': 'Institution', 'major':'Speciality' }


EducationFormSet = modelformset_factory(Education, form=EducationForm, formset=MyModelFormSet, max_num=10)


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


SkillFormSet = modelformset_factory(Skill, form=SkillForm, formset=MyModelFormSet, max_num=15)


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


LanguageFormSet = modelformset_factory(Language, form=LanguageForm, formset=MyModelFormSet, max_num=15)


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

ProjectFormSet = modelformset_factory(Project, form=ProjectForm, formset=MyModelFormSet, max_num=10)


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

PublicationFormSet = modelformset_factory(Publication, form=PublicationForm, formset=MyModelFormSet, max_num=10)


class CourseForm(ModelForm):
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

CourseFormSet = modelformset_factory(Course, form=CourseForm, formset=MyModelFormSet, max_num=10)


class HobbyForm(ModelForm):
    
    class Meta:
        model = Hobby
        fields = [
            'name',
            'cv',
            ]
        widgets = {'cv': forms.HiddenInput(),}
        labels = {'name': 'Hobby'}

HobbyFormSet = modelformset_factory(Hobby, form=HobbyForm, formset=MyModelFormSet, max_num=10)


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

CustomFormSet = modelformset_factory(CustomSection, form=CustomForm, formset=MyModelFormSet, max_num=10)



class TemplateChoiceForm(forms.Form):
    template = forms.ChoiceField(choices=CV_CHOICES, required=True)
    class Meta:
        model = Cv
        fields = ['template', ]

