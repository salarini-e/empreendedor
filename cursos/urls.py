from django.contrib import admin
from django.urls import path
from . import views
 
app_name='cursos'
urlpatterns = [
    path('', views.index, name='home'),
    path('area-do-estudante/', views.area_do_estudante, name='area_do_estudante'),
    path('editar-cadastro/', views.editar_cadastro, name='editar_cadastro'),
    path('editar-senha/', views.alterar_senha, name='alterar_senha'),
    path('editar-cadastro-pessoa/', views.editar_cadastro_pessoa, name='editar_cadastro_pessoa'),
    path('atividade/cevest/', views.cursos_cevest, name="cursos_cevest"),            
    path('atividade/cursos/', views.cursos, name="cursos"),            
    path('atividade/<tipo>/<filtro>', views.cursos_filtrado, name="filtrar"),            
    path('atividade/<tipo>/<id>/detalhe', views.curso_detalhe, name="curso_detalhe"),            
    path('atividade/<tipo>/<id>/matricular', views.matricular, name="matricula"),   
             
    # path('prematricula/', views.prematricula, name="prematricula"),
    path('ensino-superior/', views.ensino_superior, name="ensino_superior"),
    path('ensino-tecnico/', views.ensino_tecnico, name="ensino_tecnico"),
    path('curriculo-vitae/', views.curriculo_vitae, name="curriculo_vitae"),
    path('exportar_excel/', views.exportar_para_excel, name='exportar_excel'),
    path('exportar_excel/por-turma/', views.exportar_para_excel_por_turma, name='exportar_excel_por_turma'),

    path('cidade-inteligente/', views.cidade_inteligente_home, name='cidade_inteligente'),
    path('cidade-inteligente/cadastro-camera/', views.cidade_inteligente_cadastro_camera, name='cidade_inteligente_cadastro_camera'),
]