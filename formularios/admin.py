from django.contrib import admin
from .models import CadastroPCA

@admin.register(CadastroPCA)
class CadastroPCAAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'orgao_requisitante', 
        'subsecretaria_departamento', 
        'celular_whatsapp', 
        'email', 
        'objeto_licitacao', 
        'registro_preco', 
        'preco_estimado', 
        'prazo_execucao', 
        'programa_trabalho', 
        'data_prevista_certame', 
        'fonte_recurso', 
        'origem_preco_referencia', 
        'ata_registro', 
        'outro', 
        'dt_register'
    )
    list_filter = (
        'registro_preco', 
        'origem_preco_referencia', 
        'data_prevista_certame', 
        'fonte_recurso'
    )
    search_fields = (
        'orgao_requisitante', 
        'subsecretaria_departamento', 
        'celular_whatsapp', 
        'email', 
        'objeto_licitacao', 
        'preco_estimado', 
        'programa_trabalho', 
        'data_prevista_certame', 
        'fonte_recurso', 
        'ata_registro', 
        'outro'
    )
    ordering = ('-dt_register',)
    readonly_fields = ('dt_register',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.user = request.user
        super().save_model(request, obj, form, change)
