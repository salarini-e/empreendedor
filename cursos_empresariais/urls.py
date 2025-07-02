from django.contrib import admin
from django.urls import path
from . import views
 
app_name='cursos_empresariais'
urlpatterns = [
    path('cursos/empresariais/', views.cursos, name='home'),
    path('cursos/empresariais/area-do-estudante/', views.area_do_estudante, name='area_do_estudante'),
    path('cursos/empresariais/editar-cadastro/', views.editar_cadastro, name='editar_cadastro'),
    path('cursos/empresariais/editar-senha/', views.alterar_senha, name='alterar_senha'),
    path('cursos/empresariais/editar-cadastro-pessoa/', views.editar_cadastro_pessoa, name='editar_cadastro_pessoa'),
    path('cursos/empresariais/atividade/<tipo>', views.cursos, name="cursos"),            
    path('cursos/empresariais/atividade/<tipo>/<filtro>', views.cursos_filtrado, name="filtrar"),            
    path('cursos/empresariais/atividade/<tipo>/<id>/detalhe', views.curso_detalhe, name="curso_detalhe"),            
    path('cursos/empresariais/atividade/<tipo>/<id>/matricular', views.matricular, name="matricula"),            
    # path('prematricula/', views.prematricula, name="prematricula"),
    path('cursos/empresariais/ensino-superior/', views.ensino_superior, name="ensino_superior"),
    path('cursos/empresariais/ensino-tecnico/', views.ensino_tecnico, name="ensino_tecnico"),
    path('cursos/empresariais/curriculo-vitae/', views.curriculo_vitae, name="curriculo_vitae"),
    path('cursos/profissionais/empresariais/exportar_excel/', views.exportar_para_excel, name='exportar_excel'),
    path('capacitacao-empresarial/exportar_excel/por-turma/', views.exportar_para_excel_por_turma, name='exportar_excel_por_turma'),

    #ADMINISTRATIVO
    path('admin/cursos/', views.administrativo, name="administrativo2"),

    path('admin/cursos/instiuicoes', views.adm_instituicoes_listar, name="adm_instituicoes_listar"),
    path('admin/cursos/instituicao/cadastrar', views.adm_instituicao_cadastrar, name="adm_cadastrar_instituicao"),
    path('admin/cursos/instituicao/<id>', views.adm_locais_editar, name="adm_editar_instituicao"),
    path('admin/cursos/instituicao/<id>/excluir', views.adm_locais_excluir, name="adm_locais_excluir"),
    # MISSING EDITAR 

    path('admin/cursos/locais', views.adm_locais_listar, name="adm_locais_listar"),
    path('admin/cursos/local/cadastrar', views.adm_locais_cadastrar, name="cadastrar_local"),
    path('admin/cursos/local/<id>/editar', views.adm_locais_editar, name="adm_locais_editar"),
    path('admin/cursos/locai/<id>/excluir', views.adm_locais_excluir, name="adm_locais_excluir"),
    # MISSING VISUALIZAR

    path('admin/cursos/categorias', views.adm_categorias_listar, name="adm_categorias_listar"),
    path('admin/cursos/categoria/cadastrar', views.adm_categorias_cadastrar, name="cadastrar_categoria"),
    path('admin/cursos/categoria/<id>/editar', views.adm_categorias_editar, name="adm_categorias_editar"),
    path('admin/cursos/categoria/<id>/excluir', views.adm_categorias_excluir, name="adm_categorias_excluir"),
    # MISSING VISUALIZAR

    path('admin/cursos/cursos', views.adm_cursos_listar, name="adm_cursos_listar"),
    path('admin/cursos/curso/cadastrar', views.adm_cursos_cadastrar, name="adm_cursos_cadastrar"),
    path('admin/cursos/curso/<id>/editar', views.adm_curso_editar, name="adm_curso_editar"),
    path('admin/cursos/curso/<id>/visualizar', views.adm_curso_visualizar, name="adm_curso_visualizar"),
    path('admin/cursos/cursos/<id>/detalhes', views.adm_curso_detalhes, name="adm_curso_detalhes"),
    path('admin/cursos/cursos<id>/detalhes/exportar_excel/', views.adm_cursos_interessados_excel, name='adm_cursos_interessados_excel'),
    # path('cursos/<id_curso>/remover-interessado/<id>/', views.remover_interessado, name="adm_remover_interessado"),
    path('remover-interessado/<id>/', views.remover_interessado, name="adm_remover_interessado"),
    # path('curso/<id>/requisito/criar', views.adm_curso_visualizar, name="adm_curso_visualizar"),


    # MISSING VISUALIZAR e EXCLUIR

    path('admin/cursos/instrutores', views.adm_professores_listar, name="adm_professores_listar"),        
    path('admin/cursos/instrutor/cadastrar', views.adm_professores_cadastrar, name="adm_professores_cadastrar"),
    path('admin/cursos/instrutor/<id>/editar', views.adm_professores_editar, name="adm_professores_editar"),
    path('admin/cursos/instrutor/<id>/excluir', views.adm_professores_excluir, name="adm_professores_excluir"),
    # MISSING VISUALIZAR

    # -------- Serve para confirmar um aluno selecionado, transformando seu status para "Aluno" -------- #
    path('admin/cursos/selecionado/<matricula>', views.visualizar_turma_selecionado, name="adm_turma_visualizar_selecionado"),
    # -------- # -------- #

    path('admin/cursos/turmas', views.adm_turmas_listar, name="adm_turmas_listar"),
    path('admin/cursos/turmas-encerradas', views.adm_turmas_listar_encerradas, name="adm_turmas_listar_encerradas"),
    path('admin/cursos/turma/cadastrar', views.adm_turmas_cadastrar, name="adm_turmas_cadastrar"),
    path('admin/cursos/turma/<id>', views.adm_turmas_visualizar, name="adm_turma_visualizar"),
    path('admin/cursos/turma/<id>/editar', views.visualizar_turma_editar, name="adm_turma_editar"),
    path('admin/cursos/turma/<id>/excluir', views.excluir_turma, name="adm_turma_excluir"),
    path('admin/cursos/turma/<id>/realocar', views.adm_realocar, name="adm_turma_realocar"),
    path('admin/cursos/turma/<id>/gerar-certificados', views.gerar_certificados, name="gerar_certificados"),

    path('admin/cursos/turma/<id>/turno/cadastrar', views.adm_turno_cadastrar, name="adm_turno_cadastrar"),
    # MISSING VISUALIZAR, EDITAR, LISTAR E EXCLUIR

    path('admin/cursos/turma/<turma_id>/aula/cadastrar', views.adm_aula_cadastrar, name="adm_aula_cadastrar"),
    path('admin/cursos/turma/<turma_id>/aulas', views.adm_aulas_listar, name="adm_aulas_listar"),
    path('admin/cursos/turma/<turma_id>/aula/<aula_id>', views.adm_aula_visualizar, name="adm_aula_visualizar"),
    # MISSING EDITAR E EXCLUIR

    
    path('admin/cursos/justificativa/<presenca_id>/cadastrar', views.adm_justificativa_cadastrar, name="adm_justificativa_cadastrar"),
    path('admin/cursos/justificativa/<presenca_id>', views.adm_justificativa_visualizar, name="adm_justificativa_visualizar"),
    # MISSING LISTAR, EDITAR E EXCLUIR

    # path('gambiarra/02', views.gambiarra_cevest, name="adm_gambiarra_alunos"),
    path('admin/cursos/alunos', views.adm_alunos_listar, name="adm_alunos_listar"),
    path('admin/cursos/alunos/cadastrar/', views.adm_cadastro_aluno, name="adm_cadastrar_aluno"),
    path('admin/cursos/aluno/<id>', views.adm_aluno_visualizar, name="adm_aluno_visualizar"),
    path('admin/cursos/aluno/<id>/editar', views.adm_aluno_editar, name="adm_aluno_editar"),
    path('admin/cursos/aluno/<id>/matricular/', views.matricular_aluno, name="adm_aluno_matricular"),
    path('admin/cursos/aluno/<matricula>/desmatricular', views.desmatricular_aluno, name="adm_desmatricular_aluno"),
    path('capacitacao-empresarial/retirar-duplicadas/', views.retirar_duplicadas, name='retirar_duplicadas'),
]