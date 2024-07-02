from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('login/', views.login_page, name='login'),
     #path('logout/', views.logout_user, name='logout'),
     path('register/', views.register_page, name='register'),
     path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
     path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
]

