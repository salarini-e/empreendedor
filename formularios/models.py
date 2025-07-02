from django.db import models
from autenticacao.models import User

class CadastroPCA(models.Model):
    MERCADO_LOCAL = 'ML'
    COMPRA_ANTERIOR = 'CA'
    ATA_REGISTRO = 'AR'
    OUTRO = 'OT'

    ORIGEM_PRECO_CHOICES = [
        (MERCADO_LOCAL, 'Mercado Local'),
        (COMPRA_ANTERIOR, 'Compra Anterior'),
        (ATA_REGISTRO, 'Ata de Registro'),
        (OUTRO, 'Outro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    orgao_requisitante = models.CharField(max_length=255, verbose_name="Órgão Requisitante")
    subsecretaria_departamento = models.CharField(max_length=255, verbose_name="Subsecretaria/Departamento")
    celular_whatsapp = models.CharField(max_length=20, verbose_name="Celular/WhatsApp")
    email = models.EmailField(verbose_name="Email")
    objeto_licitacao = models.TextField(verbose_name="Objeto da Licitação")
    registro_preco = models.BooleanField(default=False, verbose_name="Registro de Preço")
    preco_estimado = models.CharField(max_length=255, verbose_name="Valor Estimado para Contratação (R$)", null=True)
    prazo_execucao = models.PositiveIntegerField(verbose_name="Prazo de Execução (meses)")
    programa_trabalho = models.CharField(max_length=255, verbose_name="Programa de Trabalho", null=True)

    data_prevista_certame = models.CharField(max_length=7, verbose_name="Data Prevista do Certame")
    fonte_recurso = models.CharField(max_length=255, verbose_name="Fonte do Recurso")
    
    origem_preco_referencia = models.CharField(
        max_length=2, 
        choices=ORIGEM_PRECO_CHOICES, 
        default=MERCADO_LOCAL, 
        verbose_name="Origem do Preço de Referência"
    )
    ata_registro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ata de Registro")
    outro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Outro (especificar)")
    dt_register = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

    def __str__(self):
        return f"{self.orgao_requisitante} - {self.objeto_licitacao}"
