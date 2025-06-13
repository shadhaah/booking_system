from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking, name='booking'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact/', views.contact, name='contact'),
    path('department/', views.department, name='department'),

    # New AI Q&A routes
    path('ai-qa/', views.ai_qa_local, name='ai_qa_local'),  # POST API endpoint for answering questions
    path('ask/', views.ask_page, name='ask_page'),     
    path('ask/', views.ask_page, name='ask_page'),

]
