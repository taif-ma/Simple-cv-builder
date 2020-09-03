from django.db import models
from users.models import User
from django_countries.fields import CountryField
from tinymce.models import HTMLField
#from .choices import *
from multiselectfield import MultiSelectField


SKILL_COMPETENCY_CHOICES = (
    ('', '-----'),
    (1, 'Below Average'),
    (2, 'Average'),
    (3, 'Good'),
    (4, 'Excellent'), )

LANGUAGE_COMPETENCY_CHOICES = (
  ('', '-----'),
    (1, "Beginner"),
    (2, "Elementary"),
    (3, "Intermediate"),
    (4, "Upper-Intermediate"),
    (5, "Advanced"),
    (6, "Native"),)



CV_CHOICES = (
    ('jakarta', 'Jakarta'),
    ('new_york', 'New York'),
    ('tokyo', 'Tokyo'),
    ('rome', 'Rome'),
    ('san_francisco', 'San Francisco'), )

 
SECTION_CHOICE = (
    ('work_experience', 'Experience'), 
    ('education', 'Education'),
    ('certifications', 'Certifications'),
    ('courses', 'Courses'),
    ('projects', 'Projects'), 
    ('publications', 'Publications'), 
    ('skills', 'Skills'), 
    ('languages','Languages'),
    ('hobbies','Hobbies'),
    ('custom_section', 'Custom Section'),
    )











class Cv(models.Model): 
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    template = models.CharField(max_length=250, choices=CV_CHOICES, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    sections = MultiSelectField(choices=SECTION_CHOICE, null=True, blank=True)

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    position = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    country = CountryField(blank_label='(Country)', blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    achievements = HTMLField(blank=True)
    
    

    def __str__(self):
        return self.position

    class Meta:
        verbose_name_plural = "Work Experience"
        ordering = ['-end_date', ]


class Certification(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255, blank=True)
    provider = models.CharField(max_length=255, blank=True)
    date_obtained = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_obtained', ]


class Education(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    school = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    major = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    country = CountryField(blank_label='(Country)', blank=True)
    #gpa = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = HTMLField(blank=True)

    def __str__(self):
        return self.school

    class Meta:
        verbose_name_plural = "Education"
        ordering = ['-end_date', ]


class Skill(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255, blank=True)
    competency = models.IntegerField(choices=SKILL_COMPETENCY_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255, blank=True)
    competency = models.IntegerField(choices=LANGUAGE_COMPETENCY_CHOICES, null=True, blank=True)
    read = models.BooleanField(default=False,blank=True, null=True)
    write = models.BooleanField(default=False,blank=True, null=True)
    speak = models.BooleanField(default=False,blank=True, null=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=500,null=True, blank=True)
    role = models.CharField(max_length=500, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)    
    description = HTMLField(blank=True)
    

    class Meta:
        verbose_name_plural = "Projects"
        ordering = ['-end_date', ]


class Publication(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=500,null=True, blank=True)
    publisher = models.CharField(max_length=500,null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    publication_url = models.CharField(max_length=500,null=True, blank=True)
    description = HTMLField(blank=True)
    

    class Meta:
        verbose_name_plural = "Publications"
        ordering = ['-publication_date', ]

class Hobby(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=500,null=True, blank=True)

    class Meta:
        verbose_name_plural = "Hobbies"

class CustomSection(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=500,null=True, blank=True)
    subtitle = models.CharField(max_length=500,null=True, blank=True)
    description =models.CharField(max_length=500,null=True, blank=True)


class Course(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE, blank=True)
    course_name = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)
    major = models.CharField(max_length=255, blank=True)
    country = CountryField(blank_label='(Country)', blank=True)
    #gpa = models.FloatField(null=True, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = HTMLField(blank=True)
    online_course = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name_plural = "Courses"
        ordering = ['-end_date', ]


