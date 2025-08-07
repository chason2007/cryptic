from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate_password, name='generate_password'),
    path('qrcode/', views.generate_qr_code, name='generate_qr_code'),
    path('history/', views.password_history, name='password_history'),  # New URL
]