from django.contrib import admin
from .models import Cv, Education, WorkExperience
# Register your models here.


class CvAdmin(admin.ModelAdmin):
    list_display = ['name', 'sections','id' ]
admin.site.register(Cv, CvAdmin)

class EducationAdmin(admin.ModelAdmin):
    list_display = ['school', 'department','major', 'degree' ]
admin.site.register(Education, EducationAdmin)

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'position','city' ]
admin.site.register(WorkExperience, WorkExperienceAdmin)
