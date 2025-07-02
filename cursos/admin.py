from django.contrib import admin
from .models import *

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'escolaridade', 'estado_civil', 'dt_inclusao')
    search_fields = ('pessoa', 'escolaridade', 'dt_inclusao')
    list_per_page = 20

class Turno_estabelecidoAdmin(admin.ModelAdmin):
    list_display = ('turma', 'turno')
    search_fields = ('turma', 'turno')
    list_per_page = 20
    
admin.site.register(Instituicao)
admin.site.register(Local)
admin.site.register(Categoria)
admin.site.register(Requisito)
admin.site.register(Curso)
admin.site.register(Instrutor)
admin.site.register(Turno)
admin.site.register(Turma)
admin.site.register(Turno_estabelecido, Turno_estabelecidoAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Responsavel)
admin.site.register(Matricula)
admin.site.register(Justificativa)
admin.site.register(Aula)
admin.site.register(Presenca)
admin.site.register(Alertar_Aluno_Sobre_Nova_Turma)
admin.site.register(Instituicao_Ensino_Superior)
admin.site.register(Curso_Ensino_Superior)
admin.site.register(Disciplinas)
# admin.site.register(Disponibilidade)






