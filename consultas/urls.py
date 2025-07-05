from django.urls import path
from . import views
from .views import registrar_consulta, dashboard

urlpatterns = [
    path('registrar/', views.registrar_consulta, name='registrar_consulta'),
    path('dashboard/', dashboard, name='dashboard'),  
]

