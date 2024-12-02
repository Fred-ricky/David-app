from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('login/', views.loginView, name='login'),
     path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
     path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
     path('not_authorized/', views.not_authorized_view, name='not_authorized'),
     path('logout/', views.logout_view, name='logout'),
     path('register/', views.register_page, name='register'),
    
]

