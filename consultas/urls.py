from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_consulta, name='registrar_consulta'),
]
