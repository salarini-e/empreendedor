from django import forms
from django.forms import ModelForm, ValidationError
from .models import *
from .functions.empresa import validate_CNPJ

class FormEmpresa(ModelForm):
    class Meta:
        model = Empresa
        fields = [ 'cnpj', 'nome', 'porte', 'atividade','ramo', 'outro_ramo','telefone', 'whatsapp', 'email', 'site', 'descricao',  'receber_noticias']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ', 'onkeydown':'mascara(this, icnpj)'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'onkeydown':'mascara(this, itel)'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Whatsapp', 'onkeydown':'mascara(this, itel)'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'atividade': forms.CheckboxSelectMultiple(),
            'ramo': forms.CheckboxSelectMultiple(),
        }
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        try:
            validate_CNPJ(cnpj)
        except ValidationError as e:
            raise forms.ValidationError(str(e))
        
        return cnpj
    
class FormRamos(ModelForm):
    
    class Meta:
        model = Empresa
        fields = ['ramo',]
        widgets = {
            'ramo': forms.CheckboxSelectMultiple(),
        }

class FormAlterarEmpresa(ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'porte', 'atividade','ramo', 'outro_ramo', 'telefone', 'whatsapp', 'email', 'site', 'descricao', 'receber_noticias', 'perfil_publico']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'onkeydown':'mascara(this, itel)'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Whatsapp', 'onkeydown':'mascara(this, itel)'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'perfil_publico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class FormLogoEmpresa(ModelForm):
    class Meta:
        model = Registro_no_vitrine_virtual
        fields = ['logo']

class FormCadastrarProduto(ModelForm):
    class Meta:
        model = Produto
        fields = ['imagem', 'nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
        }
        
class Faccao_Legal_Form(ModelForm):
    class Meta:
        model = Faccao_legal
        widgets={
        #  'possui_mei': forms.RadioSelect(attrs={'class': 'form-check-input', 'onclick': 'toggleCnpjDiv(this)'}),  
        'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ', 'onkeydown':'mascara(this, icnpj)', 'onblur': 'checkCNPJ(icnpj(this.value))'}),
         'user': forms.HiddenInput(),
         'tempo_que_trabalha': forms.RadioSelect(),
         'trabalha_com': forms.CheckboxSelectMultiple(),
         'equipamentos': forms.CheckboxSelectMultiple(),
         'tempo_que_trabalha': forms.RadioSelect(),
         'area': forms.RadioSelect(),   
         'tamanho_area': forms.RadioSelect(),
         'tipo_produto': forms.CheckboxSelectMultiple(),
         'situacao_trabalho': forms.RadioSelect(),
         'situacao_remuneracao': forms.RadioSelect(),
         'voce_prefere': forms.RadioSelect(),
        }
        fields = ['tempo_que_trabalha', 'trabalha_com', 'equipamentos', 'area', 'tamanho_area', 'possui_colaboradores', 'qtd_colaboradores', 'tipo_produto', 'outro_produto', 'situacao_trabalho', 'situacao_remuneracao', 'voce_prefere', 'user', 'possui_mei', 'cnpj', 'qual_seu_sonho_no_setor']
        exclude = []

class Criar_Processo_Admin_Form(ModelForm):
    class Meta:
        model = Processo_Digital
        widgets = {
            'tipo_processo': forms.HiddenInput(),
            'n_protocolo': forms.HiddenInput(),
            'profissao': forms.RadioSelect(),
            'solicitante': forms.HiddenInput(),    
            'n_inscricao': forms.HiddenInput(),    
            }   
        exclude = ['dt_solicitacao', 'boleto', 'boleto_pago']
        
class Criar_Processo_Form(ModelForm):
    class Meta:
        model = Processo_Digital
        widgets = {
            'tipo_processo': forms.HiddenInput(),
            'n_protocolo': forms.HiddenInput(),
            'solicitante': forms.HiddenInput(),
            }
        exclude = ['dt_solicitacao', 'boleto', 'boleto_pago', 'status']

class Processo_ISS_Form(ModelForm):
    class Meta:
        model = RequerimentoISS
        widgets = {
            'profissao': forms.RadioSelect(),
            'solicitante': forms.HiddenInput(),
            'n_inscricao': forms.HiddenInput(),        
            }
        exclude = ['processo', 'dt_solicitacao', 'boleto', 'boleto_pago', 'status', 'boleto_meio_ambiente', 'boleto_meio_ambiente_status', 'boleto_saude', 'boleto_saude_status']

class Criar_Processo_Docs_Form(ModelForm):
    class Meta:
        model = Processo_Status_Documentos_Anexos
        widgets = {
            'processo': forms.HiddenInput(),
            }
        
        exclude = ['user_register', 'rg_status', 'licenca_sanitaria',
                   'comprovante_endereco_status', 'diploma_ou_certificado_status', 
                   'licenca_sanitaria_status', 'espelho_iptu_status', 
                   'licenca_ambiental_status', 'comprovante_limpeza_caixa_dagua_status',
                   'comprovante_ar_condicionado_status', 'plano_gerenciamento_de_residuos_status', 
                   'licenca_santinaria_anterior_status', 'agente_att_caixa_dagua', 
                   'agente_att_ar', 'agente_att_residuos', 'agente_att_licenca_sanitaria_anterior', 
                   'agente_att_rg', 'agente_att_endereco', 'agente_att_certificado', 
                   'agente_att_iptu', 'espelho_iptu_status', 'contrato_locacao_status',
                   'conta_dagua_status', 'conta_luz_status', 'foto_status',
                   'croqui_acesso_status' ]
                   
class Criar_Andamento_Processo(ModelForm):
    class Meta:
        model = Andamento_Processo_Digital
        widgets = {
            'processo': forms.HiddenInput(),
            'servidor': forms.HiddenInput(),
            'status': forms.Select(attrs={'class': 'form-control', 'onchange':'exibirInput()'}),
            }
        exclude = ['dt_andamento']

class Criar_Andamento_Processo_Sanitario(ModelForm):

    STATUS_CHOICES = (
        ('aa', 'Aguardando avaliação'),
        ('ar', 'Aguardando reenvio de documentos'),
        ('bs', 'Aguardando pagamento licença sanitária'),        
        ('ls', 'Aguardando emissão licença sanitária'),        
        ('se', 'Licença ambiental sanitária'),
    )

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'onchange':'exibirInput()'}))

    class Meta:
        model = Andamento_Processo_Digital
        widgets = {
            'processo': forms.HiddenInput(),
            'servidor': forms.HiddenInput(),
            'status': forms.Select(attrs={'class': 'form-control', 'onchange':'exibirInput()'}),
            }
        exclude = ['dt_andamento']

class Criar_Andamento_Processo_Ambiental(ModelForm):

    STATUS_CHOICES = (
        ('aa', 'Aguardando avaliação'),
        ('ar', 'Aguardando reenvio de documentos'),        
        ('ba', 'Aguardando pagamento licença ambiental'),                
        ('la', 'Aguardando emissão licença ambiental'),        
        ('ae', 'Licença ambiental emitida'),        
    )

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'onchange':'exibirInput()'}))

    class Meta:
        model = Andamento_Processo_Digital
        widgets = {
            'processo': forms.HiddenInput(),
            'servidor': forms.HiddenInput(),
            'status': forms.Select(attrs={'class': 'form-control', 'onchange':'exibirInput()'}),
            }
        exclude = ['dt_andamento']

class Profissao_Form(ModelForm):
    class Meta:
        model = Profissao
        exclude = []
        
class Escola_Form(ModelForm):
    class Meta:
        model = Escola
        widgets={
            'responsavel': forms.HiddenInput()
        }
        exclude = ['dt_register', 'user_register', 'ativa']
        
class Solicitacao_de_Compras_Form(ModelForm):
    class Meta:
        model = Solicitacao_de_Compras
        widgets = {
            'tipo': forms.RadioSelect(),
            'escola': forms.HiddenInput(),
            'dt_envio_propostas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Data de Envio das Propostas', 'type': 'date'}),
            'dt_previsao_entrega': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Data de Previsão de Entrega', 'type': 'date'}),
            'ramo_atuacao': forms.CheckboxSelectMultiple(),
            }
        exclude = ['codigo', 'dt_solicitacao', 'user_register', 'status', 'proposta_vencedora', 'qnt_itens']
        
class Criar_Item_Solicitacao(ModelForm):
    class Meta:
        model = Item_Solicitacao
        widgets = {
            'solicitacao_de_compra': forms.HiddenInput(),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valor Unitário'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            }
        exclude = []

class RequerimentoISSQNForm(forms.ModelForm):
    class Meta:
        model = RequerimentoISSQN
        fields = [
            'solicitacao',
            'razao_social',
            'nome_fantasia',
            'cnpj',
            'inscricao_municipal',
            'endereco',
            'email',
            'telefone',
            'contador',
            'contador_email',
            'contador_telefone',
            # Adicione mais campos conforme necessário para os documentos pedidos
        ]
        widgets={
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ', 'onkeydown':'mascara(this, icnpj)'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'onkeydown':'mascara(this, itel)'}),
            'contador_telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone do Contador', 'onkeydown':'mascara(this, itel)'}),
        }
        
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        try:
            validate_CNPJ(cnpj)
        except ValidationError as e:
            raise forms.ValidationError(str(e))
        
        return cnpj
        

class DocumentosPedidoForm(forms.ModelForm):
    class Meta:
        model = DocumentosPedido
        fields = [
            'contrato_social',
            'carteira_orgao_classe',
            'alvara_localizacao',
            'informacoes_cadastrais_dos_empregados',
            'balanco_patrimonial',
            'dre',
            'balancete_analitico',
            'cnpj_copia',
            'profissionais_habilitados',
            'ir_empresa',
            'simples_nacional',
        ]

class Contrato_NotaFiscal(forms.ModelForm):
    class Meta:
        model = Contrato_de_Servico
        fields =['nota_fiscal']
        labels = {'nota_fiscal': ''}
        widgets = {
            'nota_fiscal': forms.FileInput(attrs={'class': 'm-auto mt-4 mb-3 form-control', 'style': 'max-width: 400px;'})
        }
        
class Contrato_Avaliacao(forms.ModelForm):
    class Meta:
        model = Contrato_de_Servico
        fields =['avaliacao']
        
class Form_Novas_Oportunidades(forms.ModelForm):
    class Meta:
        model = Novas_Oportunidades
        exclude = ['dt_register', 'user_register']
        widgets = {
            'cpf': forms.TextInput(attrs={'onkeydown': 'mascara(this, icpf)'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'onkeydown':'mascara(this, itel)'}),
            'atividade_manual': forms.CheckboxSelectMultiple(),
            'tipo_costura': forms.CheckboxSelectMultiple(),
            'tipo_producao_alimentos': forms.CheckboxSelectMultiple(),
            'tipo_producao_bebidas': forms.CheckboxSelectMultiple(),
            'renda_representacao': forms.RadioSelect(),
            'motivo_nao_comercializacao': forms.RadioSelect(),
            'renda_mensal': forms.RadioSelect(),
            'possui_empresa': forms.RadioSelect(),
            'comercializacao_produto': forms.RadioSelect(),
            'cep_negocio':forms.TextInput(attrs={'onkeydown': 'icep(this)'}),
        }

class Form_Credito_Facil(forms.ModelForm):
    
    # def __init__(self, user, *args, **kwargs):
    #     super(Form_Credito_Facil, self).__init__(*args, **kwargs)
    #     self.fields['empresa'].queryset = Empresa.objects.filter(user_register=user)
    
    class Meta:
        model = Credito_Facil
        exclude = ['dt_register', 'user_register']
        widgets = {
                'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ', 'onkeydown':'mascara(this, icnpj)'}),
                'telefone': forms.TextInput(attrs={'class': 'form-control', 'onkeydown':'mascara(this, itel)'}),
                'motivacao_emprestimo': forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleMotivacao(this)'}),
        }

class Form_Necessidades_das_Empresas(forms.ModelForm):
    class Meta:
        model = Necessidades_das_Empresas
        exclude = ['empresa', 'dt_inclusao', 'user_register']
        widgets = {          
            'outro': forms.CheckboxInput(attrs={'class': 'form-check-input', 'onclick': 'toggleOutro()'}),
        }

class Form_Natal_Artesao(forms.ModelForm):
    class Meta:
        model = Natal_Artesao
        exclude = ['dt_register', 'user_register']
        widgets = {
            'cpf': forms.TextInput(attrs={'onkeydown': 'mascara(this, icpf)'}),
            'o_que_pretende_comercializar': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'O que pretende comercializar?'}),
            'produto_1': forms.FileInput(attrs={'class': 'form-control'}),
            'produto_2': forms.FileInput(attrs={'class': 'form-control'}),
            'dias_que_pode_trabalhar': forms.CheckboxSelectMultiple(),
        }