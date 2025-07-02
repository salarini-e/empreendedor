from django.contrib import admin
from .models import Pessoa, MembroPCA, Consultor_Sebrae

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'telefone', 'dt_nascimento', 'bairro', 'endereco', 'numero', 'complemento', 'cep', 'dt_inclusao')
    search_fields = ('nome', 'email', 'cpf')
    list_per_page = 20

admin.site.register(Pessoa, PessoaAdmin)

class MembroPCAAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'ativo', 'dt_register')
    search_fields = ('pessoa',)
    autocomplete_fields = ['pessoa'] 
    list_per_page = 20

admin.site.register(MembroPCA, MembroPCAAdmin)

class Consultor_SebraeAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'ativo', 'dt_register')
    search_fields = ('pessoa',)
    autocomplete_fields = ['pessoa'] 
    list_per_page = 20

admin.site.register(Consultor_Sebrae, Consultor_SebraeAdmin)