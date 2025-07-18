import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django_cpf_cnpj.fields import CNPJField
import uuid
from PIL import Image
from django.core.exceptions import ValidationError

class Porte_da_Empresa(models.Model):
    porte=models.CharField(max_length=32, verbose_name='Porte da empresa')
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

    __str__ = lambda self: self.porte

class Atividade(models.Model):
    atividade=models.CharField(max_length=64, verbose_name='Atividade')
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

    __str__ = lambda self: self.atividade
    
class Ramo_de_Atuacao(models.Model):
    ramo=models.CharField(max_length=164, verbose_name='Ramo de atuação')
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    
    __str__ = lambda self: self.ramo
    
class Empresa(models.Model):
    cnpj=models.CharField(max_length=18, verbose_name='CNPJ', unique=True)
    nome=models.CharField(max_length=128, verbose_name='Nome da empresa')
    porte=models.ForeignKey(Porte_da_Empresa, on_delete=models.CASCADE, verbose_name='Porte da empresa')
    # cep = models.CharField(max_length=10, verbose_name='CEP')
    # bairro = models.CharField(max_length=128, verbose_name='Bairro')
    # endereco = models.CharField(max_length=128, verbose_name='Endereço')
    # numero = models.CharField(max_length=10, verbose_name='Número')
    # complemento = models.CharField(max_length=128, verbose_name='Complemento', null=True, blank=True)
    atividade=models.ManyToManyField(Atividade, verbose_name='Atividade')
    outra_atividade=models.CharField(max_length=64, verbose_name='Outra atividade', blank=True, null=True)
    ramo=models.ManyToManyField(Ramo_de_Atuacao, verbose_name='Ramo de atuação')
    outro_ramo=models.CharField(max_length=64, verbose_name='Outro ramo', blank=True, null=True)
    receber_noticias=models.BooleanField(default=False, verbose_name='Deseja receber notificações sobre compras da prefeitura?')
    telefone=models.CharField(max_length=15, verbose_name='Telefone de contato', null=True, blank=True)
    whatsapp=models.CharField(max_length=15, verbose_name='Whatsapp da empresa', null=True, blank=True)
    email=models.EmailField(verbose_name='E-mail da empresa', null=True, blank=True)
    site=models.URLField(verbose_name='Site da empresa', null=True, blank=True)
    descricao = models.TextField(null=True, blank=True, verbose_name='Descrição da empresa')
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    validacao=models.BooleanField(default=False, verbose_name='Validação da empresa')
    cadastrada_na_vitrine=models.BooleanField(default=False, verbose_name='Cadastrado na Vitrine Virtual?')
    cadastrada_como_fornecedor=models.BooleanField(default=False, verbose_name='Cadastrado como fornecedor da prefeitura?')
    perfil_publico=models.BooleanField(default=False, verbose_name='Permitir que o perfil seja público?')
    
    __str__ = lambda self: f'{self.nome} - {self.cnpj}'
    
class Registro_no_vitrine_virtual(models.Model):
    empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    logo=models.ImageField(upload_to='logos/', verbose_name='Logo da empresa', null=True, blank=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)

class Produto(models.Model):
    rg_vitrine=models.ForeignKey(Registro_no_vitrine_virtual, on_delete=models.CASCADE, verbose_name='Registro da vitrine virtual')
    nome=models.CharField(max_length=128, verbose_name='Nome do produto ou serviço')
    descricao=models.TextField(verbose_name='Descrição do produto')
    imagem=models.ImageField(upload_to='produtos/', verbose_name='Imagem do produto')
    validacao_da_equipe=models.BooleanField(default=False, verbose_name='Validação da Sala do Empreendedor')
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)

class Trabalho_Faccao(models.Model):
    nome = models.CharField(max_length=128, verbose_name='Nome do trabalho')
    def __str__(self) -> str:
        return self.nome
    
class Equipamentos_Faccao(models.Model):
    nome = models.CharField(max_length=128, verbose_name='Nome do equipamento')
    def __str__(self) -> str:
        return self.nome
    
class Tipo_produto_faccao(models.Model):
    nome = models.CharField(max_length=128, verbose_name='Nome do produto')
    def __str__(self) -> str:
        return self.nome
    
class Faccao_legal(models.Model):
    
    TEMPO_CHOICES=(
        ('0','Menos de 1 ano'),
        ('1','De 1 a 3 anos'),
        ('2','Mais de 3 anos'),
    )
    AREA_CHOICES=(
        ('s', 'Sim'),
        ('n', 'Não'),
    )
    TAMANHO_AREA_CHOICES=(
        ('0', 'Menos de 6m²'),
        ('1', 'De 6 a 16m²'),
        ('2', 'De 16 a 50m²'),
        ('3', 'Mais de 50m²'),
    )
    QNT_COLABORADORES_CHOICES=(
        ('0', '1 a 2'),
        ('1', '3 a 4'),
        ('2', '5 a 10'),
        ('3', 'Mais de 10'),
    )
    SITUACAO_CHOICES=(
        ('p', 'Pouco'),
        ('s', 'Suficiente'),
        ('d', 'Em demasia'),    
    )
    REMUNERACAO_CHOICES=(
        ('bx', 'Baixo'),
        ('rg', 'Regular'),
        ('bo', 'Bom'),
        ('ot', 'Ótimo')   
    )
    VOCE_PREFERE_CHOICES=(
        ('ccf', 'Continuar como faccionista.'),
        ('eec', 'Estar empregado em uma confecção.'),   
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário', null=True)
    possui_mei=models.BooleanField(default=False, verbose_name='Possui MEI ou empresa de outro porte?')
    cnpj=models.CharField(max_length=18, verbose_name='CNPJ', null=True, blank=True)
    tempo_que_trabalha=models.CharField(max_length=1, blank=False, verbose_name='Trabalha com facção há quanto tempo', choices=TEMPO_CHOICES)
    trabalha_com = models.ManyToManyField(Trabalho_Faccao, verbose_name='Trabalha com:', null=True)
    equipamentos = models.ManyToManyField(Equipamentos_Faccao, verbose_name='Quais equipamentos possui?')
    area = models.CharField(max_length=1, verbose_name='Possui área de trabalho separada da residência?', choices=AREA_CHOICES)
    tamanho_area = models.CharField(max_length=1, verbose_name='Qual o tamanho da área de trabalho?', choices=TAMANHO_AREA_CHOICES)
    possui_colaboradores = models.BooleanField(default=False, verbose_name='Possui colaboradores?')
    qtd_colaboradores = models.IntegerField(verbose_name='Quantos colaboradores possui?', null=True, blank=True)
    tipo_produto = models.ManyToManyField(Tipo_produto_faccao, verbose_name='Que tipos de produtos produz?')
    outro_produto = models.CharField(max_length=128, verbose_name='Produz outro produto? Caso sim, descreva:', null=True, blank=True)
    situacao_trabalho = models.CharField(max_length=1, verbose_name='Geralmente, como está de trabalho?', choices=SITUACAO_CHOICES)
    situacao_remuneracao = models.CharField(max_length=2, verbose_name='Como considera a renda que obtêm com seu trabalho?', choices=REMUNERACAO_CHOICES)
    voce_prefere = models.CharField(max_length=3, verbose_name='Você prefere:', choices=VOCE_PREFERE_CHOICES) 
    qual_seu_sonho_no_setor = models.TextField(verbose_name='Qual seu sonho no setor?', null=True, blank=True)
    
#PROCESSOS
class Agente_Ambiental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Agente Ambiental')
    email = models.EmailField(verbose_name="Email para receber notificação de processo", null=True)
    ativo = models.BooleanField(default=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

class Agente_Tributario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Agente Tributário')
    email = models.EmailField(verbose_name="Email para receber notificação de processo", null=True)
    ativo = models.BooleanField(default=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

class Agente_Divida_Fiscal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Agente Fiscal de Dívida')
    email = models.EmailField(verbose_name="Email para receber notificação de processo", null=True)
    ativo = models.BooleanField(default=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

class Agente_Procuradoria(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Agente Procurador')
    email = models.EmailField(verbose_name="Email para receber notificação de processo", null=True)
    ativo = models.BooleanField(default=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

class Agente_Sanitario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Agente Sanitário')
    email = models.EmailField(verbose_name="Email para receber notificação de processo", null=True)
    ativo = models.BooleanField(default=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

class Agente_Cartorio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Agente de Cartório')
    email = models.EmailField(verbose_name="Email para receber notificação de processo", null=True)
    ativo = models.BooleanField(default=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

class Escolaridade(models.Model):

    nome=models.CharField(max_length=128, verbose_name='Nome da escolaridade')
    
    def __str__(self) -> str:
        return self.nome

class Status_do_processo(models.Model):

    nome=models.CharField(max_length=128, verbose_name='Status')
    
    def __str__(self) -> str:
        return self.nome
    
class Profissao(models.Model):
    
    escolaridade = models.ForeignKey(Escolaridade, on_delete=models.CASCADE, verbose_name='Escolaridade')
    nome = models.CharField(max_length=128, verbose_name='Nome da profissão')
    licenca_sanitaria = models.BooleanField(default=False, verbose_name='Necessita licença sanitária?')    
    licenca_sanitaria_com_alvara = models.BooleanField(default=False, verbose_name='Quando com alvará necessita licença sanitária?')
    licenca_ambiental = models.BooleanField(default=False, verbose_name='Necessita licença ambiental?')
    # licenca_ambiental_com_alvara = models.BooleanField(default=False, verbose_name='Quando com alvará necessita licença sanitária?')

    class Meta:
        ordering = ['nome']
        
    def __str__(self) -> str:
        return self.nome

#Ordem ao cadastrar o Tipo de Processo    
# 1 - Requerimento ISS
# 2 - Baixa de ISS
# 3 - Requerimento ISSQN    
class Tipo_Processos(models.Model):
        
        nome = models.CharField(max_length=128, verbose_name='Nome do processo')
        descricao = models.TextField(verbose_name='Descrição do processo')
        dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
        user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)
                
        def __str__(self) -> str:
            return self.nome

class Administrador(models.Model):
    
    pessoa = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Pessoa', related_name='pessoa_adm')
    processos_autorizados = models.ManyToManyField(Tipo_Processos, verbose_name='Processos autorizados')
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True, related_name='user_register_adm')
        
class Processo_Digital(models.Model):
    
    # PROCESSO_CHOICES=(
    #     ('0', 'Requerimento de ISS'),
    #     ('1', 'Cancelamento de ISS'),
    # )
    STATUS_CHOICES=(
        ('nv', 'Novo'),
        ('ae', 'Aguardando envio de documentos'),
        ('ar', 'Aguardando reenvio de documentos'),
        ('aa', 'Aguardando avaliação'),
        ('bs', 'Aguardando pagamento licença sanitária'),
        ('ba', 'Aguardando pagamento licença ambiental'),
        ('sa', 'Aguardando pagamento licença ambiental e licença ambiental'),
        ('ls', 'Aguardando emissão licença sanitária'),
        ('la', 'Aguardando emissão licença ambiental'),                
        ('se', 'Licença sanitária emitida'),
        ('ae', 'Licença ambiental emitida'),
        ('bg', 'Boleto gerado'),    
        ('cn', 'Concluído')
    )
    status = models.CharField(max_length=2, verbose_name='Status', choices=STATUS_CHOICES, default='nv')
    tipo_processo = models.ForeignKey(Tipo_Processos, on_delete=models.CASCADE, verbose_name='Tipo de processo')
    # tipo_processo=models.CharField(max_length=1, verbose_name='Tipo de processo', choices=PROCESSO_CHOICES)
    n_protocolo=models.CharField(max_length=128, verbose_name='Número do protocolo', null=True, blank=True)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário', null=True)
    dt_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de solicitação', null=True)
    dt_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de atualização', null=True)
    
    def __str__(self) -> str:
        return self.n_protocolo    

    def save(self, *args, **kwargs):
        self.dt_atualizacao = timezone.now()
        super(Processo_Digital, self).save(*args, **kwargs)
        
class RequerimentoISS(models.Model):
    
    AUTONOMO_LOCALIZADO_CHOICES=(
        ('s', 'Sim'),
        ('n', 'Não'),   
    )
    
    processo = models.ForeignKey(Processo_Digital, on_delete=models.CASCADE, verbose_name='Processo', null=True)     
    profissao = models.ForeignKey(Profissao, on_delete=models.CASCADE, verbose_name='Profissão')
    autonomo_localizado = models.CharField(max_length=1, verbose_name='Autônomo localizado?', choices=AUTONOMO_LOCALIZADO_CHOICES)
    boleto = models.FileField(upload_to='processos/boleto/', verbose_name='Boleto', null=True, blank=True)
    boleto_saude = models.FileField(upload_to='processos/boleto/saude', verbose_name='Boleto vigilância sanitária', null=True, blank=True)
    boleto_saude_status = models.BooleanField(default=False, verbose_name='Boleto vigilância sanitária pago?')
    boleto_meio_ambiente = models.FileField(upload_to='processos/boleto/meio-ambiente', verbose_name='Boleto meio ambiente', null=True, blank=True)
    boleto_meio_ambiente_status = models.BooleanField(default=False, verbose_name='Boleto meio ambiente pago?')
    boleto = models.FileField(upload_to='processos/boleto/', verbose_name='Boleto', null=True, blank=True)
    # boleto_pago = models.BooleanField(default=False, verbose_name='Boleto pago?')
    n_inscricao = models.CharField(max_length=128, verbose_name='Número de inscrição', null=True, blank=True)
    dt_solicitacao = models.DateField(auto_now_add=True, verbose_name='Data de solicitação', null=True)
    dt_atualizacao = models.DateField(auto_now=True, verbose_name='Data de atualização', null=True)
    
    def save(self, *args, **kwargs):
        self.dt_atualizacao = timezone.now()
        super(RequerimentoISS, self).save(*args, **kwargs)
        
class Andamento_Processo_Digital(models.Model):
    STATUS_CHOICES=(
        ('nv', 'Novo'),
        ('ae', 'Aguardando envio de documentos'),
        ('ar', 'Aguardando reenvio de documentos'),
        ('aa', 'Aguardando avaliação'),
        ('bs', 'Aguardando pagamento licença sanitária'),
        ('ba', 'Aguardando pagamento licença ambiental'),
        ('sa', 'Aguardando pagamento licença ambiental e licença ambiental'),
        ('ls', 'Aguardando emissão licença sanitária'),
        ('la', 'Aguardando emissão licença ambiental'),
        ('se', 'Licença ambiental sanitária'),
        ('ae', 'Licença ambiental emitida'),
        ('bg', 'Boleto gerado'),
        ('cn', 'Concluído')
    )
    processo = models.ForeignKey(Processo_Digital, on_delete=models.CASCADE, verbose_name='Processo')
    status = models.CharField(max_length=2, verbose_name='Status', choices=STATUS_CHOICES, default='nv') 
    observacao = models.TextField(verbose_name='Mensagem', default='n/h')
    servidor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Servidor', blank=True, null=True)
    dt_andamento = models.DateField(auto_now=True, verbose_name='Data de atualização')
    
    def __str__(self) -> str:
        return str(self.processo.n_protocolo) + ' - ' +str(self.id) + ' - ' + str(self.dt_andamento)

#Documentos do Requerimento de ISS
class LimitedImageField(models.ImageField):
    def __init__(self, *args, **kwargs):
        self.allowed_formats = kwargs.pop('allowed_formats', ['jpeg', 'png'])
        self.max_size = kwargs.pop('max_size', None)
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value:
            image = Image.open(value)
            format = image.format.lower()
            if format not in self.allowed_formats:
                raise ValidationError(f'A imagem deve estar nos formatos {", ".join(self.allowed_formats)}.')

            if image.size[0] > self.max_size[0] or image.size[1] > self.max_size[1]:
                raise ValidationError(f'A imagem não pode ser maior que {self.max_size[0]}x{self.max_size[1]} pixels.')

class Processo_Status_Documentos_Anexos(models.Model):
    DOC_STATUS_CHOICES=(
        ('0', 'Aguardando avaliação'),
        ('1', 'Aprovado'),
        ('2', 'Reprovado'),
        ('3', 'Atualização requerida'),
    )
    processo = models.ForeignKey(Processo_Digital, on_delete=models.CASCADE, verbose_name='Processo')
    user_register = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)
    rg = models.FileField(upload_to='processos/rg_cnh/', verbose_name='RG/CNH/Passaporte', null=True)
    comprovante_endereco = models.FileField(upload_to='processos/comprovante_endereco/', verbose_name='Comprovante de endereço', null=True)
    diploma_ou_certificado = models.FileField(upload_to='processos/diploma_ou_certificado/', verbose_name='Diploma ou certificado', null=True, blank=True)
    # Licença Sanitária
    licenca_sanitaria = models.FileField(upload_to='processos/licenca_sanitaria/', verbose_name='Licença sanitária', null=True, blank=True)
    comprovante_limpeza_caixa_dagua = models.FileField(upload_to='processos/licenca_sanitaria/', verbose_name="Laudo de serviço e comprovante de limpeza de caixa d'agua por firma credenciada no INEA", null=True, blank=True)
    comprovante_limpeza_caixa_dagua_status = models.CharField(max_length=1, verbose_name="Status Limpeza Caixa d'Agua", choices=DOC_STATUS_CHOICES, default='0')
    agente_att_caixa_dagua = models.ForeignKey(Agente_Sanitario, related_name="caixa_dagua_anexos", on_delete=models.CASCADE, verbose_name="Agente que autalizou o status da caixa d'água", null=True)
    comprovante_ar_condicionado = models.FileField(upload_to='processos/licenca_sanitaria/', verbose_name="Comprovante de manutenção de ar condicionado", null=True, blank=True)
    comprovante_ar_condicionado_status = models.CharField(max_length=1, verbose_name='Status Comprovante Ar Condicionado', choices=DOC_STATUS_CHOICES, default='0')
    agente_att_ar = models.ForeignKey(Agente_Sanitario, related_name="ar_anexos", on_delete=models.CASCADE, verbose_name="Agente que autalizou o status da manutenção do ar", null=True)
    plano_gerenciamento_de_residuos = models.FileField(upload_to='processos/licenca_sanitaria/', verbose_name="Plano de ferenciamento de resíduos", null=True, blank=True)
    plano_gerenciamento_de_residuos_status = models.CharField(max_length=1, verbose_name='Status Gerenciamento de Resíduos', choices=DOC_STATUS_CHOICES, default='0')
    agente_att_residuos = models.ForeignKey(Agente_Sanitario, related_name="residuos_anexos", on_delete=models.CASCADE, verbose_name="Agente que autalizou o status do plano de resíduos", null=True)
    licenca_santinaria_anterior = models.FileField(upload_to='processos/licenca_sanitaria/', verbose_name="Licença sanitária anterior (para renovação)", null=True, blank=True)
    licenca_santinaria_anterior_status = models.CharField(max_length=1, verbose_name='Status Licenca Sanitária Anterior', choices=DOC_STATUS_CHOICES, default='0')
    agente_att_licenca_sanitaria_anterior = models.ForeignKey(Agente_Sanitario, related_name="licenca_sanitaria_anexos", on_delete=models.CASCADE, verbose_name="Agente que autalizou o status da antiga licença sanitária", null=True)
    # Fim Licenca Sanitária
    # Licença Ambiental
    licenca_ambiental = models.FileField(upload_to='processos/licenca_ambiental/', verbose_name='Licença ambiental', null=True, blank=True)
    espelho_iptu = models.FileField(upload_to='processos/espelho_iptu/', verbose_name='Espelho do IPTU', null=True, blank=True)
    espelho_iptu_status = models.CharField(max_length=1, verbose_name='Status Licenca Sanitária Anterior', choices=DOC_STATUS_CHOICES, default='0')
    contrato_locacao = models.FileField(upload_to='processos/contrato-locacao/', verbose_name='Cópia do contrato de locação, se houver', null=True, blank=True)
    contrato_locacao_status = models.CharField(max_length=1, verbose_name='Status Licenca Sanitária Anterior', choices=DOC_STATUS_CHOICES, default='0')
    conta_dagua = models.FileField(upload_to='processos/conta-dagua/', verbose_name="Conta d'água", null=True, blank=True)
    conta_dagua_status = models.CharField(max_length=1, verbose_name='Status Licenca Sanitária Anterior', choices=DOC_STATUS_CHOICES, default='0')
    conta_luz = models.FileField(upload_to='processos/conta-luz/', verbose_name='Conta de luz', null=True, blank=True)
    conta_luz_status = models.CharField(max_length=1, verbose_name='Status Licenca Sanitária Anterior', choices=DOC_STATUS_CHOICES, default='0')
    foto = LimitedImageField(upload_to='processos/fotos_empresa/', null=True, blank=True, verbose_name="Foto da empresa para possibilitar a vistoria do técnico (jpg ou png)", help_text='Limite: 2MB', allowed_formats=['jpeg', 'jpg', 'png'], max_size=(2048, 2048))
    foto_status = models.CharField(max_length=1, verbose_name='Status Licenca Sanitária Anterior', choices=DOC_STATUS_CHOICES, default='0')
    croqui_acesso = LimitedImageField(upload_to='processos/croqui_acesso/', null=True, blank=True, verbose_name="Croqui de acesso para possibilitar a localização e vistoria da local de atuação. (jpg ou png)", help_text='Limite: 2MB', allowed_formats=['jpeg', 'jpg', 'png'], max_size=(2048, 2048))
    croqui_acesso_status = models.CharField(max_length=1, verbose_name='Status Licenca Sanitária Anterior', choices=DOC_STATUS_CHOICES, default='0')
    # Fim Licença Ambiental
    
    rg_status=models.CharField(max_length=1, verbose_name='Status do RG', choices=DOC_STATUS_CHOICES, default='0')
    agente_att_rg = models.ForeignKey(Agente_Tributario, related_name="rg_anexos", on_delete=models.CASCADE, verbose_name="Agente que autalizou o status do RG", null=True)
    comprovante_endereco_status=models.CharField(max_length=1, verbose_name='Status do comprovante de endereço', choices=DOC_STATUS_CHOICES, default='0')
    agente_att_endereco = models.ForeignKey(Agente_Tributario, related_name="comprovante_endereco_anexos", on_delete=models.CASCADE, verbose_name="Agente que autalizou o status do comprovante de endereço", null=True)
    diploma_ou_certificado_status=models.CharField(max_length=1, verbose_name='Status do diploma ou certificado', choices=DOC_STATUS_CHOICES, default='0')
    agente_att_certificado = models.ForeignKey(Agente_Tributario, related_name="certificado_anexos", on_delete=models.CASCADE, verbose_name="Agente que autalizou o status do Certificado/Diploma", null=True)
    licenca_sanitaria_status=models.CharField(max_length=1, verbose_name='Status da licença sanitária', choices=DOC_STATUS_CHOICES, default='0')
    licenca_ambiental_status=models.CharField(max_length=1, verbose_name='Status da licença ambiental', choices=DOC_STATUS_CHOICES, default='0')
    espelho_iptu_status=models.CharField(max_length=1, verbose_name='Status do espelho do IPTU', choices=DOC_STATUS_CHOICES, default='0')
    agente_att_iptu = models.ForeignKey(Agente_Tributario, related_name="iptu_anexos", on_delete=models.CASCADE, verbose_name="Agente que autalizou o status do Espelho de IPTU", null=True)

class RequerimentoISSQN(models.Model):
    SOLICITACAO_CHOICES=(
        ('r', 'Renovação'),
        ('i', 'Inscrição')
    )
    processo = models.ForeignKey(Processo_Digital, on_delete=models.CASCADE, verbose_name='Processo', null=True)
    solicitacao = models.CharField(max_length=1, verbose_name='Tipo de solicitação', choices=SOLICITACAO_CHOICES)
    razao_social = models.CharField(max_length=255, verbose_name='Razão social')
    nome_fantasia = models.CharField(max_length=255, verbose_name='Nome fantasia')
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ')
    inscricao_municipal = models.CharField(max_length=20, verbose_name='Inscrição municipal')
    endereco = models.CharField(max_length=255, verbose_name='Endereço')
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    contador = models.CharField(max_length=255, verbose_name='Contador')
    contador_email = models.EmailField(verbose_name='E-mail do contador')
    contador_telefone = models.CharField(max_length=20, verbose_name='Telefone do contador')
    boleto = models.FileField(upload_to='processos/boleto/', verbose_name='Boleto', null=True, blank=True)
    dt_register = models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    user_register = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)
    
    def __str__(self):
        return self.razao_social
    
#Documentos do Requerimento de ISSQN    
class DocumentosPedido(models.Model):
    DOC_STATUS_CHOICES=(
        ('0', 'Aguardando avaliação'),
        ('1', 'Aprovado'),
        ('2', 'Reprovado'),
        ('3', 'Atualização requerida'),
    )
    requerimento = models.ForeignKey(RequerimentoISSQN, on_delete=models.CASCADE, verbose_name='Requerimento')
    contrato_social = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='1. Contrato social ou última alteração contratual')
    contrato_social_status = models.CharField(max_length=1, verbose_name='Status do contrato social', choices=DOC_STATUS_CHOICES, default='0')
    carteira_orgao_classe = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='2. Carteira do órgão de classe (CREA, CRM, OAB, etc.)')
    carteira_orgao_classe_status = models.CharField(max_length=1, verbose_name='Status da carteira do órgão de classe', choices=DOC_STATUS_CHOICES,  default='0')
    alvara_localizacao = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='3. Alvará de localização e funcionamento')
    alvara_localizacao_status = models.CharField(max_length=1, verbose_name='Status do alvará de localização e funcionamento', choices=DOC_STATUS_CHOICES,  default='0')
    informacoes_cadastrais_dos_empregados = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='4. Informações cadastrais dos empregados (RAS/e-Social/SEFIP)')
    informacoes_cadastrais_dos_empregados_status = models.CharField(max_length=1, verbose_name='Status das informações cadastrais dos empregados', choices=DOC_STATUS_CHOICES,  default='0')
    balanco_patrimonial = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='5. Balanço patrimonial compelto (último exercício), discriminado')
    balanco_patrimonial_status = models.CharField(max_length=1, verbose_name='Status do balanço patrimonial', choices=DOC_STATUS_CHOICES,  default='0')
    dre = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='6. DRE completo (último exercício), discriminado')
    dre_status = models.CharField(max_length=1, verbose_name='Status do DRE', choices=DOC_STATUS_CHOICES,  default='0')
    balancete_analitico = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='7. Balancete analítico completo (último exercício), discriminado')
    balancete_analitico_status = models.CharField(max_length=1, verbose_name='Status do balancete analítico', choices=DOC_STATUS_CHOICES,  default='0')
    cnpj_copia = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='8. Cópia do CNPJ')
    cnpj_copia_status = models.CharField(max_length=1, verbose_name='Status da cópia do CNPJ', choices=DOC_STATUS_CHOICES,  default='0')
    profissionais_habilitados = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='9. Relação dos profissionais habilitados (CREA, CRM, OAB, etc.)')
    profissionais_habilitados_status = models.CharField(max_length=1, verbose_name='Status da relação dos profissionais habilitados', choices=DOC_STATUS_CHOICES,  default='0')
    ir_empresa = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='10. IR da empresa (último exercício), discriminado')
    ir_empresa_status = models.CharField(max_length=1, verbose_name='Status do IR da empresa', choices=DOC_STATUS_CHOICES,  default='0')
    simples_nacional = models.FileField(upload_to='documentos/requerimento_issqn/', verbose_name='11. Simples nacional (último exercício), discriminado')
    simples_nacional_status = models.CharField(max_length=1, verbose_name='Status do simples nacional', choices=DOC_STATUS_CHOICES,  default='0')
    
    def __str__(self):
        return f'Documentos Pedido - {self.requerimento.razao_social}'
    
@receiver(post_save, sender=Processo_Digital)
def generate_process_number(sender, instance, created, **kwargs):
    if created and not instance.n_protocolo:  # Verifica se o objeto foi criado recentemente e se o número do processo já existe
        random_part = ''.join(random.choices(string.digits, k=5))
        # print('ID:', instance.id)
        n_protocolo='{}{}'.format(random_part, instance.id)
        aux=len(n_protocolo)
        if aux>8:
            while aux>8:
                n_protocolo = n_protocolo[1:]
                aux=len(n_protocolo)
        instance.n_protocolo='{:8}'.format(n_protocolo.zfill(8))
        instance.save()

@receiver(post_save, sender=Andamento_Processo_Digital)
@receiver(post_save, sender=Processo_Status_Documentos_Anexos)
def atualizar_dt_atualizacao_processo(sender, instance, **kwargs):
    instance.processo.dt_atualizacao = timezone.now()
    instance.processo.save()
    
    
## Modelos do PDDE    
class Escola(models.Model):
    
    nome = models.CharField(max_length=128, verbose_name='Razão social')
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ', unique=True)
    cep = models.CharField(max_length=10, verbose_name='CEP')
    endereco = models.CharField(max_length=128, verbose_name='Endereço')
    bairro = models.CharField(max_length=128, verbose_name='Bairro')
    telefone = models.CharField(max_length=128, verbose_name='Telefone', null=True, blank=True)
    email = models.EmailField(verbose_name='E-mail', blank=True, null=True)
    dt_register = models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Responsável pelas compras', null=True, related_name='responsavel_escola')
    user_register = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True, related_name='user_register_escola')
    ativa=models.BooleanField(default=False, verbose_name='Registro ativo ou validado?')
    def __str__(self) -> str:
        return self.nome
    
class Solicitacao_de_Compras(models.Model):
    STATUS_CHOICES=(
        ('0', 'Criando solicitação'),
        ('1', 'Aguardando propostas'),
        ('2', 'Aguardando analise de propostas'),
        # ('3', 'Aguardando avaliação de contrato'),
        ('3', 'Aguardando aceite de contrato'),
        ('4', 'Aguardando entrega/serviço'),
        ('5', 'Aguardando efetuamento do pagamento'),
        ('6', 'Aguardando nota fiscal'),
        ('7', 'Aguardando avaliação de serviço'),
        ('8', 'Processo concluído'),
    )
    TIPO_CHOICES=(
        ('s', 'Serviço'),
        ('p', 'Produto'),
    )
    PRECO_CHOICES=(
        ('i', 'item'),
        ('l', 'lote'),
    )
    
    codigo = models.CharField(max_length=20, unique=True, null=True)
    status = models.CharField(max_length=1, verbose_name='Status da solicitacao', choices=STATUS_CHOICES, default='0')
    tipo = models.CharField(max_length=1, verbose_name='Tipo', choices=TIPO_CHOICES)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, verbose_name='Escola')
    descricao = models.TextField(verbose_name='Descrição')
    dt_envio_propostas = models.DateField(verbose_name='Data limite para envio de propostas')
    previsao_entrega = models.IntegerField(verbose_name='Previsão de quantos dias para entrega após fechar o contrato?', default=0)
    qnt_itens = models.IntegerField(verbose_name='Quantidade de itens solicitados', null=True, blank=True)
    proposta_vencedora = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa com proposta vencedora', null=True, blank=True)
    ramo_atuacao = models.ManyToManyField(Ramo_de_Atuacao, verbose_name='Enviar mensagem para as empresas com os seguintes ramos de atuação:', null=True, blank=True)
    dt_solicitacao = models.DateField(auto_now_add=True, verbose_name='Data de solicitação')
    
    def gerar_codigo_solicitacao(self):
        codigo = str(uuid.uuid4().hex)[:12].upper()
        codigo = "PDDE-" + codigo

        return codigo
    
    def is_fim_propostas(self):
        hoje = timezone.now().date()
        print('---------------------------')
        print('model: ', self.dt_envio_propostas, ' today: ', hoje)
        return self.dt_envio_propostas == hoje

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.gerar_codigo_solicitacao()
        super(Solicitacao_de_Compras, self).save()
        
class Item_Solicitacao(models.Model):
    
    solicitacao_de_compra = models.ForeignKey(Solicitacao_de_Compras, on_delete=models.CASCADE, verbose_name='Solicitação de compra')
    nome = models.CharField(max_length=128, verbose_name='Nome do item')
    quantidade = models.IntegerField(verbose_name='Quantidade')
    unidade = models.CharField(max_length=128, verbose_name='Unidade de medida')
    descricao = models.TextField(verbose_name='Descrição')
 
class Proposta(models.Model):
    qnt_itens_proposta = models.IntegerField(verbose_name='Quantidade de itens propostos')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    solicitacao_de_compra = models.ForeignKey(Solicitacao_de_Compras, on_delete=models.CASCADE, verbose_name='Solicitação de compra')
    previsao_entrega = models.IntegerField(verbose_name='Previsão de quantos dias para entrega após fechar o contrato?', default=0)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
        
class Proposta_Item(models.Model):
    proposta = models.ForeignKey(Proposta, on_delete=models.CASCADE, verbose_name='Proposta')
    item_solicitacao = models.ForeignKey(Item_Solicitacao, on_delete=models.CASCADE, verbose_name='Item da compra')
    preco = models.IntegerField(verbose_name='Preço/Proposta')
    
    
class Contrato_de_Servico(models.Model):
    AVALIACAO_CHOICES =(
        ('0', 'Dentro da espectativa'),
        ('1', 'Acima da espectativa')
    )
    solicitacao_referente = models.ForeignKey(Solicitacao_de_Compras, on_delete=models.CASCADE, verbose_name='Solicitação de compra')
    proposta_vencedora = models.ForeignKey('Proposta', on_delete=models.CASCADE, verbose_name='Proposta')
    itens_solicitados = models.ManyToManyField('Item_Solicitacao', verbose_name='Itens do contrato')
    propostas_itens = models.ManyToManyField('Proposta_Item', verbose_name='Propostas dos itens')
    titulo = models.CharField(max_length=128, verbose_name='Título')
    proposito= models.TextField(verbose_name='Proposito')
    aceito_pela_empresa = models.BooleanField(default=False, verbose_name='Contrato aceito pela empresa?')
    hash = models.CharField(max_length=128, verbose_name='Hash do contrato', null=True)
    nota_fiscal = models.FileField(upload_to='contratos_pdde/nota_fiscal/', verbose_name='Nota fiscal', null=True)
    avaliacao = models.CharField(max_length=1, verbose_name='Avaliação do serviço', choices=AVALIACAO_CHOICES, null=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True)

# CLASSES RELACIONADAS A NOVAS OPORTUNIDADES
class AtividadeManual(models.Model):
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.descricao

## Relacionado a Atividade Manual
class Tipo_Costura(models.Model):
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.descricao
    
class Tipo_Producao_Alimentos(models.Model):
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.descricao

class Tipo_Producao_Bebidas(models.Model):
    descricao = models.CharField(max_length=100)
    def __str__(self):
        return self.descricao
## FIM Relacionado a Atividade Manual
    
class Novas_Oportunidades(models.Model):
    RENDA_REPRESENTACAO_CHOICES=(
        ('toda_renda', 'Toda a minha renda.'),
        ('maior_parte', 'A maior parte da minha renda.'),
        ('menor_parte', 'A menor parte da minha renda.'),
        ('nao_comercializa', 'Ainda não atuo de forma comercial.')
    )
    MOTIVO_NAO_COMERCIALIZACAO_CHOICES=(
        ('Ja_comercializa', 'Já comercializo, como dito anteriormente'),        
        ('atuando_outra_area', 'Estou atuando profissionalmente em outra área')   ,
        ('nao_sei_empreender', 'Não sei como empreender, por isso tenho receio de não dar certo'),
        ('outro', 'Outro motivo')
    )
    RENDA_MENSAL_CHOICES=(
        ('0', 'Até meio salário mínimo (até R$706,00 reais)'),
        ('1', 'De meio salário a 1 salário mínimo (de R$707,00 a R$1.412,00)'),
        ('2', 'De 1 a 2 salários mínimos (de R$1.413,00 a R$2.824,00)'),
        ('3', 'De 2 a 4 salários mínimos (de R$2.825,00 até R$5.648,00)'),
        ('4', 'De 4 a 7 salários mínimos (de r$4.649,00 até R$9.884,00)'),
        ('5', 'Acima de 7 salários mínimos (R$9.885,00 ou mais)'),
        ('6', 'Não sei ou prefiro não responder')
    )
    POSSUI_EMPRESA_CHOICES =(
        ('s', 'Sim'),
        ('n', 'Não')
    )
    COMERCIALIZACAO_PRODUTO_CHOICES =(
        ('casa_online', 'Em casa (vendo online)'),
        ('ponto_comercial', 'Possuo um ponto comercial fixo'),
        ('ponto_ambulante', 'Ponto fixo de ambulante'),
        ('ambulante_movel', 'Ambulante móvel'),
        ('feiras', 'Feiras'),
        ('expositor_outros', 'Expositor fixo em outros pontos comerciais'),
    )
    
    cpf=models.CharField(max_length=14, verbose_name='CPF', null=True)
    telefone=models.CharField(max_length=15, verbose_name='Telefone de contato/whatsapp', null=True, blank=True)
    email=models.EmailField(verbose_name='E-mail para contato')
    atividade_manual = models.ManyToManyField(AtividadeManual, verbose_name='1. Atualmente você desenvolve alguma atividade ou produção manual (pode assinalar quantas alternativas você achar necessário)?')
    tipo_costura = models.ManyToManyField(Tipo_Costura, verbose_name='1. Qual tipo de costura?', null=True, blank=True)
    tipo_producao_alimentos = models.ManyToManyField(Tipo_Producao_Alimentos, verbose_name='1. Qual tipo de produção de alimentos?', null=True, blank=True)
    tipo_producao_bebidas = models.ManyToManyField(Tipo_Producao_Bebidas,   verbose_name='1. Qual tipo de produção de bebidas?', null=True, blank=True)
    renda_representacao = models.CharField(max_length=20, choices=RENDA_REPRESENTACAO_CHOICES, verbose_name='2. Essa atividade manual representa:')
    motivo_nao_comercializacao = models.CharField(max_length=50, choices=MOTIVO_NAO_COMERCIALIZACAO_CHOICES, verbose_name='3. Se ainda não comercializa, qual o motivo?')
    renda_mensal = models.CharField(max_length=1, choices=RENDA_MENSAL_CHOICES, verbose_name='4. Qual é a sua renda mensal? (Inclua nesse cálculo a soma de dinheiro de todas as suas fontes de renda, como salários, produção manual, pensão de filhos, benefício temporário do governo, etc.)')
    possui_empresa = models.CharField(max_length=1, choices=POSSUI_EMPRESA_CHOICES, verbose_name='5. Possui uma empresa ou MEI para venda dos seus produtos e atividades?')
    comercializacao_produto = models.CharField(max_length=30, choices=COMERCIALIZACAO_PRODUTO_CHOICES, verbose_name='6. Como você comercializa seus produtos? (marque todas as opções que se adequem a você)')
    cep_negocio = models.CharField(max_length=9, verbose_name='7. Qual o CEP do seu negócio?')
    alavancar_negocio = models.TextField(verbose_name='8. O que você acha que poderia ser feito para ajudar o seu negócio a alavancar?')
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True, blank=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

    def __str__(self):
        return f"Formulário - {self.id}"
    
    def save(self, *args, **kwargs):
        try:
            item = Novas_Oportunidades.objects.get(cpf=self.cpf)
            item.delete()
        except:
            pass
        super(Novas_Oportunidades, self).save(*args, **kwargs)
    

class Credito_Facil(models.Model):
    
    MOTIVACAO_CHOICES = (
        ('cg', 'Capital de Giro'),
        ('in', 'Investimento em equipamento/obra'),
        ('rf', 'Requilibrio financeiro'),
        ('ou', 'Outro'),
    )
    
    cnpj=models.CharField(max_length=18, verbose_name='CNPJ da empresa', null=True)
    telefone=models.CharField(max_length=15, verbose_name='Telefone de contato/whatsapp', null=True, blank=True)
    email=models.EmailField(verbose_name='E-mail para contato')
    valor_desejado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor desejado (R$)')
    motivacao_emprestimo = models.CharField(max_length=2, choices=MOTIVACAO_CHOICES, verbose_name='Motivação do empréstimo')
    outra_motivacao = models.CharField(max_length=128, verbose_name='Qual outra motivação do emprestivo?', null=True, blank=True)
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True, blank=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    
    def __str__(self):
        return f"Crédito Fácil - {self.cnpj} - R${self.valor_desejado} - {self.dt_register}"
    
class Necessidades_das_Empresas(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=True)
    user_register = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True, blank=True)
    capacitacao_empresarial = models.BooleanField(default=False, verbose_name='Capacitação empresarial')
    capacitacao_profissional = models.BooleanField(default=False, verbose_name='Capacitação profissional')
    credito = models.BooleanField(default=False, verbose_name='Crédito')
    consultoria = models.BooleanField(default=False, verbose_name='Consultoria')
    outro = models.BooleanField(default=False, verbose_name='Outro')
    outro_descricao = models.CharField(max_length=128, verbose_name='Qual outra necessidade?', null=True, blank=True)
    dt_inclusao = models.DateField(auto_now_add=True, verbose_name='Data de inclusão')

    def __str__(self):
        return f"Necessidades das Empresas - {self.id}"

class diasDaSemanaNatal_Artesao(models.Model):
    label_semana = models.CharField(max_length=128, verbose_name='Dia da semana', null=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    
    def __str__(self):
        return f"{self.label_semana}"
    
class Natal_Artesao(models.Model):
    cpf=models.CharField(max_length=14, verbose_name='CPF', null=True)
    o_que_pretende_comercializar = models.TextField(verbose_name='O que pretende comercializar?')
    produto_1 = models.ImageField(upload_to='produtos_natal_artesao/', verbose_name='Foto do produto 1', null=True, blank=True)
    produto_2 = models.ImageField(upload_to='produtos_natal_artesao/', verbose_name='Foto do produto 2', null=True, blank=True)
    user_register=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário que cadastrou', null=True, blank=True)
    dias_que_pode_trabalhar = models.ManyToManyField(diasDaSemanaNatal_Artesao, verbose_name='Quais dias da semana você tem disponibilidade para estar na feira?', null=True)
    dt_register=models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
    
    def __str__(self):
        return f"Natal Artesão - {self.id}"