from django.urls import path
from . import views
from users import views as user_views


urlpatterns = [
    


    path('my-cvs', views.my_cvs, name='my-cvs'),
    path('cv-preview/<int:pk>', views.cv_preview, name='cv_preview'),    
    path('cv/template-choice/<int:pk>/', views.change_template, name='change_template'),
    path('add-cv/', views.add_cv, name='add_cv'),    
    
    path('add-experience/<int:pk>/', views.work_experience, name='work_experience'),
    path('add-education/<int:pk>/', views.education, name='education'), 
    
    
    #path('add-certifications/<int:pk>/', views.certifications, name='certifications'), 
    #path('add-skills/<int:pk>/', views.skills, name='skills'), 
    #path('add-languages/<int:pk>/', views.languages, name='languages'), 
    #path('add-projects/<int:pk>/', views.projects, name='projects'), 
    #path('add-hobbies/<int:pk>/', views.hobbies, name='hobbies'), 
    #path('add-courses/<int:pk>/', views.courses, name='courses'), 
    #path('add-publications/<int:pk>/', views.publications, name='publications'), 
    #path('add-custom-section/<int:pk>/', views.custom_section, name='custom_section'), 

    
    
    path('cv/delete/<int:pk>/', views.delete_cv, name='delete-cv'),
]
