from django.urls import path
from . import views
from users import views as user_views
#from wkhtmltopdf.views import PDFTemplateView

#from .views import resume_template_choice

from main.pdf_views import download_pdf

from main.docx_views import  download_docx

urlpatterns = [
    

    #### Create CV ####
    path('my-cvs', views.my_cvs, name='my-cvs'),
    path('cv-preview/<int:pk>', views.cv_preview, name='cv_preview'),    
    path('cv/template-choice/<int:pk>/', views.change_template, name='change_template'),
    path('add-cv/', views.add_cv, name='add_cv'),    
    path('cv-done/<int:pk>/', views.cv_done, name='cv_done'),
    path('add-experience/<int:pk>/', views.work_experience, name='work_experience'),
    path('add-education/<int:pk>/', views.education, name='education'), 
    path('add-certifications/<int:pk>/', views.certifications, name='certifications'), 
    path('add-skills/<int:pk>/', views.skills, name='skills'), 
    path('add-languages/<int:pk>/', views.languages, name='languages'), 
    path('add-projects/<int:pk>/', views.projects, name='projects'), 
    path('add-hobbies/<int:pk>/', views.hobbies, name='hobbies'), 
    path('add-courses/<int:pk>/', views.courses, name='courses'), 
    path('add-publications/<int:pk>/', views.publications, name='publications'), 
    path('add-custom-section/<int:pk>/', views.custom_section, name='custom_section'), 

    
    
    #path('cv/pdf/<int:pk>/', views.GeneratePdf.as_view(), name='GeneratePdf'),
    #path('cv/pdf-test/<int:pk>/', views.cv_view_pdf, name='cv_view_pdf'),

    #path('cv/easypdf/<int:pk>', views.MyPDF.as_view(), name='MyPDF'),
    #path('cv/download/<int:pk>', views.pdf_download, name='pdf_download'),
    #path('cv/generate/<int:pk>/', views.cv_pdf, name='cv_pdf'), # avec le  service payant

    
    
    #path('cv/viewpdf/<int:pk>/', views.ViewPdf.as_view(), name='ViewPdf'), 
    
    #path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('cv/delete/<int:pk>/', views.delete_cv, name='delete-cv'),
    #path('cv/create/', views.CvWizard.as_view(views.FORMS), name='create-cv'),
    #path('cv/create/template', views.cv_template_choice, name='cv_template_choice'),
    #path('edit/cv/<int:pk>/', views.CvWizard.as_view(views.FORMS), name='edit-cv'),
    #path('edit/cv/<int:pk>/template', views.cv_template_choice, name='cv_template_choice'),
    #path('faq/', views.faq, name='faq'),
    #path('templates/', views.templates, name='templates'),
    #path('payment/', user_views.payment, name='payment'),
    #path('payment/notification/', user_views.payment_notification, name='payment-notif'),
    path('cv/<int:pk>/choose/', views.choose, name='choose'),
    path('cv/<int:pk>/view-cv/', views.choose, name='view-cv'),


    path('download/pdf/<int:pk>', download_pdf, name='download_pdf'),
    path('download/docx/<int:pk>', download_docx, name='download_docx'),


    
]
