from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Porte_da_Empresa)
admin.site.register(Atividade)
admin.site.register(AtividadeManual)
admin.site.register(Ramo_de_Atuacao)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'porte', 'receber_noticias', 'validacao', 'cadastrada_na_vitrine', 'cadastrada_como_fornecedor']
    search_fields = ['nome', 'cnpj']
    list_filter = ['porte', 'validacao', 'cadastrada_na_vitrine', 'cadastrada_como_fornecedor']
    list_editable = ['validacao', 'cadastrada_na_vitrine', 'cadastrada_como_fornecedor']
    
admin.site.register(Empresa, EmpresaAdmin)

class ProdutoVitrineAdmin(admin.ModelAdmin):
    list_display = ['nome', 'user_register' ]
    search_fields = ['nome', 'user_register']
    
admin.site.register(Produto, ProdutoVitrineAdmin)
admin.site.register(Registro_no_vitrine_virtual)
admin.site.register(Trabalho_Faccao)
admin.site.register(Equipamentos_Faccao)
admin.site.register(Tipo_produto_faccao)
admin.site.register(Faccao_legal)
admin.site.register(Escolaridade)
admin.site.register(Profissao)
admin.site.register(Processo_Digital)
admin.site.register(Status_do_processo)
admin.site.register(Andamento_Processo_Digital)
admin.site.register(Tipo_Processos)
admin.site.register(Administrador)
admin.site.register(Processo_Status_Documentos_Anexos)
admin.site.register(Solicitacao_de_Compras)
admin.site.register(Item_Solicitacao)
admin.site.register(Proposta)
admin.site.register(Proposta_Item)
admin.site.register(Escola)
admin.site.register(Contrato_de_Servico)
admin.site.register(RequerimentoISS)
admin.site.register(RequerimentoISSQN)
admin.site.register(DocumentosPedido)
admin.site.register(Novas_Oportunidades)
admin.site.register(Credito_Facil)
admin.site.register(Agente_Sanitario)
admin.site.register(Agente_Tributario)
admin.site.register(Agente_Ambiental)
admin.site.register(diasDaSemanaNatal_Artesao)
admin.site.register(Natal_Artesao)