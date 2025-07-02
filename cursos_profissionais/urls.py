from django.urls import path
from . import views

app_name = 'cursos_profissionais'
urlpatterns = [
    path('cursos/profissionais/', views.index, name='index'),
    path('cursos/profissionais/<id>/inscricao', views.inscrever, name='inscrever'),
]