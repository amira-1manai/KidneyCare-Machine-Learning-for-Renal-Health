from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.deshboard, name="dashboard"),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name='logout'),
    path('doctor_dashboard/', views.doctor_dashboard_view, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard_view, name='patient_dashboard'),
    # Patient Pages Show 
    path('patinettest/', views.patinetTest, name='patinettest'), 
    path('presults/', views.Presults, name='presults'), 
    path('preport/', views.Preport, name='preport'), 
    path('disease_progression/', views.disease_progression, name='disease_progression'), 

     # Docter Pages Show 
    path('dallpaitensreports/', views.DAllpaitensReports, name='dallpaitensreports'),

    # One Time User 
    path('onetimeuser/', views.OneTimeUser, name='onetimeuser'),

]