from django.contrib import admin
from .models import Cv, Education, WorkExperience, Certification
# Register your models here.

class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
class CertificationInline(admin.TabularInline):
    model = Certification
class EducationInline(admin.TabularInline):
    model = Education

class CvAdmin(admin.ModelAdmin):
    list_display = ['name', 'sections','id' ]
    inlines = [WorkExperienceInline, EducationInline, CertificationInline]

admin.site.register(Cv, CvAdmin)

class EducationAdmin(admin.ModelAdmin):
    list_display = ['school', 'department','major', 'degree' ]
admin.site.register(Education, EducationAdmin)

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'position','city' ]
admin.site.register(WorkExperience, WorkExperienceAdmin)
