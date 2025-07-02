from django.shortcuts import render
from django.db import connection
from .api import ApiProtocolo
from .views_folder.minha_empresa import *
from .views_folder.vitrine_virtual import *
from .views_folder.admin import *
from .forms import Faccao_Legal_Form, Escola_Form, Solicitacao_de_Compras_Form,Criar_Item_Solicitacao, Criar_Processo_Docs_Form, RequerimentoISSQNForm, DocumentosPedidoForm, Processo_ISS_Form
from django.urls import reverse
from autenticacao.functions import validate_cpf
from .models import Profissao, Escola, Solicitacao_de_Compras, Item_Solicitacao, Proposta, Proposta_Item, Contrato_de_Servico, Tipo_Processos, Processo_Status_Documentos_Anexos, RequerimentoISS
from .functions.pdde import Listar_Proposta, PDDE_POST
from django.db import transaction
from guardiao.models import TentativaBurla

# Create your views here.
def index(request):
    context = {
         'titulo': 'Sala do Empreendedor - Página Inicial',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/index.html', context)

def conheca_nossa_sala(request):
    context = { 
        'titulo': 'Sala do Empreendedor - Conheça nossa sala',   
    }
    return render(request, 'sala_do_empreendedor/conheca-nossa-sala.html', context)

def em_construcao(request):
    context = {
         'titulo': 'Sala do Empreendedor - Em construção',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/em-construcao.html', context)

def consultar_protocolo(request):
    api = ApiProtocolo()
    status, response = api.recuperarAssuntos()
    print(response)
    message=response['message']
    if request.method == 'POST':
        
        status, message = api.recuperarProcesso(request.POST['cpf'])
        
    context = {
         'titulo': 'Sala do Empreendedor - Consultar Protocolo',
         'status': status,
         'message': message
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/consultar-protocolo.html', context)


def faccao_legal(request):
    context = {
        'titulo': 'Sala do Empreendedor - Facção Legal',
        'titulo_pag':'Facção Legal',
    }
    if request.method == 'POST':
        try:
            pessoa=Pessoa.objects.get(cpf=validate_cpf(request.POST['cpf']))
            messages.warning(request, 'Faça seu login antes de cadastrar sua facção')
            next_page = reverse('autenticacao:login') + f'?next={reverse("empreendedor:cadastrar_faccao_legal")}'
            return redirect(next_page)
        except Exception as E:
            print(E)
            next_page = reverse('autenticacao:cadastrar_usuario') + f'?next={reverse("empreendedor:cadastrar_faccao_legal")}'
            return redirect(next_page)

    return render(request, 'sala_do_empreendedor/faccao_legal.html', context)

@login_required
def cadastrar_faccao_legal(request):
    if request.method == 'POST':
        form = Faccao_Legal_Form(request.POST)
        if form.is_valid():
            faccao = form.save(commit=False)
            faccao.user = request.user
            faccao.save()            
            try:
                if request.POST['cadastrar_empresa'] == 'on':
                    messages.success(request, 'Facção cadastrada com sucesso! Agora efetue o cadastro da empresa.')
                    return redirect('empreendedor:cadastrar_empresa')
            except:
                messages.success(request, 'Facção cadastrada com sucesso!')
            return redirect('empreendedor:index')
    else:
        form = Faccao_Legal_Form(initial={'user': request.user.id})
    context = {
        'titulo': 'Sala do Empreendedor - Cadastrar Facção Legal',
        'titulo_pag':'Facção Legal',
        'form': form,
    }
    return render(request, 'sala_do_empreendedor/cadastro_faccao_legal.html', context)

import json
from django.http import JsonResponse
import re

def checkProfissao(request):    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        try:
            profissao = Profissao.objects.get(id=id)
        except:
            profissao = False
        if profissao:
            if profissao.escolaridade.id == 1 or profissao.escolaridade.id == 2 or profissao.escolaridade.id == 3 or profissao.escolaridade.id == 4:
                diploma = True
            else: 
                diploma = False
            response_data = {'exists': True, 'licenca_sanitaria': profissao.licenca_sanitaria, 'diploma': diploma, 'licenca_ambiental': profissao.licenca_ambiental}
        else:
            response_data = {'exists': False}

        return JsonResponse(response_data)
    return JsonResponse({})

def checkCPF(request):    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        cpf = data.get('cpf')
        try:
            pessoa = Pessoa.objects.get(cpf=re.sub(r'[^0-9]', '', cpf))
        except:
            pessoa = False
        print(cpf, pessoa)
        if pessoa:
            response_data = {'exists': True, 'nome': pessoa.nome}
        else:
            response_data = {'exists': False}

        return JsonResponse(response_data)
    return JsonResponse({})

def checkCNPJ(request):    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        cnpj = data.get('cnpj')
        try:
            empresa = Empresa.objects.get(cnpj=re.sub(r'[^0-9]', '', cnpj))
        except:
            empresa = False
        if empresa:
            response_data = {'exists': True}
        else:
            response_data = {'exists': False}

        return JsonResponse(response_data)
    return JsonResponse({})

def cadastro_fornecedores_e_compras_publicas(request):
    context = {
        'titulo': 'Cadastro de Fornecedores e Compras Públicas',
        'titulo_pag':'Cadastro de Fornecedores e Compras Públicas',
    }
    return render(request, 'sala_do_empreendedor/cadastro_fornecedores_e_compras.html', context)

def iss_autonomos(request):
    context = {
        'titulo': 'Sala do Empreendedor - ISS ou Autônomos',
        'titulo_pag':'ISS ou Autônomo',
    }
    return render(request, 'sala_do_empreendedor/iss_autonomos.html', context)

def legislacao(request):
    context = {
        'titulo': 'Sala do Empreendedor - Legislação',
        'titulo_pag':'Legislação',
    }
    return render(request, 'sala_do_empreendedor/legislacao.html', context)

def oportunidade_de_negocios(request):
    context = {
        'titulo': 'Sala do Empreendedor - Oportunidade de Negócios',
        'titulo_pag':'Oportunidade de Negócios',
    }
    return render(request, 'sala_do_empreendedor/oportunidade_de_negocios.html', context)

def vitrine_virtual(request):
    registros=Registro_no_vitrine_virtual.objects.all().order_by('?')
    empresa_e_produtos=[]
    for registro in registros:
        produtos=Produto.objects.filter(rg_vitrine=registro)
        # print(produtos)
        if registro.logo:
            try:
                empresa_e_produtos.append({"empresa": registro.empresa, "logo": str(registro.logo.url), "produtos": produtos})
            except:
                pass
        else:
            try:
                empresa_e_produtos.append({"empresa": registro.empresa, "logo": None, "produtos": produtos})
            except:
                pass
            
    paginator = Paginator(empresa_e_produtos, 100) 
    page = request.GET.get('page')
    registros_paginated = paginator.get_page(page)

    context = {
        'titulo': 'Sala do Empreendedor - Vitrine Virtual',
        'titulo_pag': 'Vitrine Virtual',
        'registros': registros_paginated,
    }
    return render(request, 'sala_do_empreendedor/vitrine-virtual/vitrine.html', context)

def quero_ser_mei(request):
    context = {
         'titulo': 'Sala do Empreendedor - Quero ser MEI',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei.html', context)

#views do QUERO SER MEI
def por_que_ser_mei(request):
    context = {
         'titulo': 'Sala do Empreendedor',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/por-que-ser-mei.html', context)
def o_que_precisa_saber_para_ser_mei(request):
    context = {
         'titulo': 'Sala do Empreendedor - O que você precisa saber para ser MEI',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/o-que-voce-precisa-saber-antes-de-se-tornar-um-mei.html', context)
def jornada_empreendedora(request):
    context = {
         'titulo': 'Sala do Empreendedor - Jornada Empreendedora',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/jornada-empreendedora.html', context)
def documentosNecessarios(request):
    context = {
         'titulo': 'Sala do Empreendedor - Documentos Necessários',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/documentosNecessarios.html', context)

def quaisAsOcupacoesQuePodemSerMei(request):
    context = {
        'titulo':'Sala do Empreendedor - Quais as ocupações que podem ser MEI',
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/quaisAsOcupacoesQuePodemSerMei.html', context)

def dicasDeSegurancaDaVigilanciaSanitaria(request):
    context = {
        'titulo':'Sala do Empreendedor - Dicas de Segurança da Vigilância Sanitária',
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/dicasDeSegurancaDaVigilanciaSanitaria.html', context)

def dicasDeSegurançaDoCorpoDeBombeiros(request):
    context = {
        'titulo':'Sala do Empreendedor - Dicas de Segurança do Corpo de Bombeiros',
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/dicasDeSegurançaDoCorpoDeBombeiros.html', context)

def dicasDeMeioAmbiente(request):
    context = {
        'titulo':'Sala do Empreendedor - Dicas de Meio Ambiente',
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/dicasDeMeioAmbiente.html', context)

def prepareSe(request):
    context = {
        'titulo':'Sala do Empreendedor - Quero Ser MEI - Prepare-se',
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/prepareSe.html', context)

def transportadorAutonomoDeCargas(request):
    context = {
        'titulo':'Sala do Empreendedor - Quero Ser MEI - Transportador Autônomo de Cargas',
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/transportadorAutonomoDeCargas.html', context)

def direitosEObrigacoes(request):
    context = {
        'titulo':'Sala do Empreendedor - Quero Ser MEI - Direitos e Obrigações',
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/direitosEObrigacoes.html', context)

def registrocadastur(request):
    context = {
         'titulo': 'Sala do Empreendedor - Quero Ser MEI - Registro Cadastur',
    }
    return render(request, 'sala_do_empreendedor/quero-ser-mei/registrocadastur.html', context)

def ja_sou_mei(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já sou MEI',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/ja-sou-mei.html', context)

def emissaoDeComprovante(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Emissão de Comprovante',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/emissaoDeComprovante.html', context)

def atualizacaoCadastral(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Atualização Cadastral',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/atualizacaoCadastral.html', context)

def capacita(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Capacita',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/capacita.html', context)

def notaFiscal(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Nota Fiscal',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/notaFiscal.html', context)

def relatorioMensal(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Relatório Mensal',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/relatorioMensal.html', context)

def pagamentoDeContribuicaoMensal(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Pagamento de Contribuição Mensal',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/pagamentoDeContribuicaoMensal.html', context)

def solucoesFinanceiras(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Soluções Financeiras',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/solucoesFinanceiras.html', context)

def certidoesEComprovantes(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Certidões e Comprovantes',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/certidoesEComprovantes.html', context)

def declaracaoAnualDeFaturamento(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Declaração Anual de Faturamento',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/declaracaoAnualDeFaturamento.html', context)

def dispensaDeAlvara(request):
    context = {
         'titulo': 'Sala do Empreendedor - Já  Sou Mei - Dispensa de Alvará',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/jaSouMei/dispensaDeAlvara.html', context)

def abertura_de_empresa(request):
    context = {
         'titulo': 'Sala do Empreendedor - Abertura de Empresa',
        # 'titulo': apps.get_app_config('financas').verbose_name,
    }
    return render(request, 'sala_do_empreendedor/abertura-de-empresa.html', context)

@login_required()
def requerimento_iss(request):
    if request.method == 'POST':
        form = Criar_Processo_Form(request.POST, request.FILES)
        form_iss = Processo_ISS_Form(request.POST, request.FILES)
        if form.is_valid() and form_iss.is_valid():
            processo = form.save(commit=False)
            processo.tipo_processo = Tipo_Processos.objects.get(id=1)
            processo.solicitante = request.user
            processo.save()
            processo_iss = form_iss.save(commit=False)
            processo_iss.processo = processo
            processo_iss.save() 
            messages.success(request, 'Processo iniciado. Agora, envie os documentos necessários.')
            andamento = Andamento_Processo_Digital(
                processo=processo,              
                status='ae',
                observacao = 'Processo iniciado. Aguardando envio de documentos.',
                servidor = None
            )
            andamento.save()
            # status=Processo_Status_Documentos_Anexos(processo=processo)
            # status.save()
            return redirect('empreendedor:requerimento_iss_doc', n_protocolo=processo.n_protocolo) 
        else:
            print(form.errors)
    else:
        form = Criar_Processo_Form(initial={'tipo_processo': 1, 'solicitante': request.user.id})
        form_iss = Processo_ISS_Form(initial={'solicitante': request.user.id})
    context = {
        'titulo': 'Sala do Empreendedor - Requerimento de ISS',
        'form': form,
        'form_iss': form_iss,
    }
    return render(request, 'sala_do_empreendedor/processos_digitais/cadastro_processo.html', context)

def requerimento_iss_documentos(request, n_protocolo):
    processo=Processo_Digital.objects.get(n_protocolo=n_protocolo)
    requerimento_iss = RequerimentoISS.objects.get(processo=processo)
    if request.method == 'POST':
        form = Criar_Processo_Docs_Form(request.POST, request.FILES)
        if form.is_valid():
            documentos = form.save(commit=False)
            documentos.processo = processo
            documentos.user_register = request.user
            documentos.save()
            messages.success(request, 'Processo criado com sucesso!')
            andamento = Andamento_Processo_Digital(
                processo=processo,              
                status='nv',
                observacao = 'Processo criado. Aguardando avaliação do pedido.',
                servidor = None
            )
            andamento.save()
            status=Processo_Status_Documentos_Anexos(processo=processo)
            status.save()
            return redirect('empreendedor:processos_digitais_admin')
        else:
            print(form.errors)
    else:
        form = Criar_Processo_Docs_Form(initial={'processo': processo.id, 'user_register': request.user.id})
    print(requerimento_iss.profissao.escolaridade.id)
    if requerimento_iss.profissao.escolaridade.id in [1,2,3,4]:
        print('Tem diploma')
        not_diploma = False
    else:
        print('Não tem diploma')
        not_diploma = True
    context = {
        'titulo': 'Sala do Empreendedor - Requerimento de ISS',
        'form': form, 
        'processo': processo,
        'requerimento': requerimento_iss,
        'not_diploma': not_diploma
    }
    return render(request, 'sala_do_empreendedor/processos_digitais/cadastro_processo_doc.html', context)


def andamento_processo_iss(request, processo):
    requerimento_iss = RequerimentoISS.objects.get(processo=processo)
    andamentos = Andamento_Processo_Digital.objects.filter(processo=processo).order_by('-id')
    status_documentos = Processo_Status_Documentos_Anexos.objects.get(processo=processo)
    context = {
        'titulo': 'Sala do Empreendedor - Andamento do Processo Online',
        'processo': processo,
        'andamentos': andamentos,
        'status_documentos': status_documentos,
        'requerimento': requerimento_iss,
    }
    return render(request, 'sala_do_empreendedor/processos_digitais/andamento_processo_iss.html', context)

@login_required()
def andamento_processo(request, protocolo):
    processo = Processo_Digital.objects.get(n_protocolo=protocolo)
    if processo.tipo_processo.id == 1:
        andamento_processo_iss(request, processo)
    return redirect('empreendedor:listar_processos')

@login_required
def atualizar_documento_processo(request, protocolo, doc):
    try:
        processo = Processo_Digital.objects.get(n_protocolo = protocolo)
        status = Processo_Status_Documentos_Anexos.objects.get(processo = processo)
        try:
            status_doc = getattr(status, f"{doc}_status")
        except:
            messages.warning(request, 'Este documento não existe.')
            TentativaBurla.objects.create(
                local_deteccao=f'empreendedor:atualizar_documento_processo -> /sala-do-empreendedor/processos-digitais/{protocolo}/att-doc/{doc}',
                user=request.user,
                ip_address=request.META.get('REMOTE_ADDR'),
                informacoes_adicionais=f'Possivel tentativa de acessar arquivo alterando url. Documento não encontrado: {doc}'
            )
            return redirect('empreendedor:andamento_processo', protocolo=protocolo)
        if status_doc == '2':
            if request.method == 'POST':
                # Validar se o arquivo é válido antes de atualizar
                novo_documento = request.FILES[doc]
                # Faça a validação necessária, por exemplo, tipo de arquivo, tamanho, etc.
                        
                with transaction.atomic():
                    # Atualizar o documento
                    setattr(processo, doc, novo_documento)
                    processo.save()

                    # Mudar o status para 'Aguardando avaliação'
                    setattr(status, f"{doc}_status", '0')
                    status.save()

                # Muda o status para 'Aguardando avaliação'
                setattr(status, f"{doc}_status", '0')
                status.save()
                processo.save()
                # Verifica se todos os documentos estão aprovados para poder seguir com o processo
                is_reprovado = (
                    status.rg_status == '2' or
                    status.comprovante_endereco_status == '2' or
                    status.diploma_ou_certificado_status == '2' or
                    status.licenca_sanitaria == '2' or
                    status.espelho_iptu_status == '2'
                )
                # Se não há documento reprovado, o processo pode seguir
                if not is_reprovado:
                    # Criasse então um novo andamento para o processo
                    Andamento_Processo_Digital.objects.create(
                        processo=processo,              
                        status='aa', 
                        observacao = 'Processo atualizado. Aguardando nova avaliação dos documentos.',
                        servidor = None
                    )            
                    processo.status = 'aa'
                    processo.save()
                    messages.success(request, 'Documento enviado com sucesso! Aguarde a nova avaliação dos documentos.')
                else:
                    messages.warning(request, 'Documento enviado com sucesso! Termine de atualizar os outros documentos.')
                return redirect('empreendedor:andamento_processo', protocolo=protocolo)
            context={
                'documento': doc
            }
            return render(request, 'sala_do_empreendedor/processos_digitais/att_documento.html', context)
        messages.warning(request, 'Este arquivo não necessita de alteração.')
        return redirect('empreendedor:andamento_processo', protocolo=protocolo)
    except Processo_Digital.DoesNotExist:
        messages.warning(request, 'Processo não encontrado.')
    except Processo_Status_Documentos_Anexos.DoesNotExist:
        messages.warning(request, 'Status de documentos não encontrado.')

    return redirect('empreendedor:andamento_processo', protocolo=protocolo)

def consultar_processos(request):
    context = {
        'titulo': 'Sala do Empreendedor - Consultar Processo Desenvolve NF',
    }
    return render(request, 'sala_do_empreendedor/processos_digitais/consultar_processo.html', context)

@login_required()
def meus_processos(request):
    proecsesos = Processo_Digital.objects.filter(solicitante=request.user).order_by('-dt_solicitacao')    
    paginator = Paginator(proecsesos, 50)
    context = {
        'titulo': 'Sala do Empreendedor - Meus Processos Online',
        'processos': paginator.get_page(request.GET.get('page')),
    }
    return render(request, 'sala_do_empreendedor/processos_digitais/listar_processos.html', context)


@login_required()
def pdde_index(request):
    cotext = {
        'titulo': 'Sala do Empreendedor - PDDE',
    }
    return render(request, 'sala_do_empreendedor/pdde/index.html', cotext)

@login_required()
def pdde_admin(request):
    cotext = {
        'titulo': 'Sala do Empreendedor - ADM - PDDE',
        'escolas': Escola.objects.all()
    }
    return render(request, 'sala_do_empreendedor/pdde/admin.html', cotext)

@login_required()
def pdde_index_escola(request):
    cotext = {
            'titulo': 'Sala do Empreendedor - PDDE Escola',
            'escolas': Escola.objects.filter(responsavel=request.user),
            # 'nome_da_escola': escola.nome,
        }
    return render(request, 'sala_do_empreendedor/pdde/index_escola.html', cotext)

@login_required()
def pdde_index_empresa(request):
    try:
        empresa = Empresa.objects.filter(user_register=request.user)
        if empresa.count() == 0:
            empresa=False
    except:
        empresa=False
    cotext = {
            'titulo': 'Sala do Empreendedor - PDDE Empresa',
            'solicitacoes': Solicitacao_de_Compras.objects.exclude(status='0'),
            'empresa': empresa
        }
    return render(request, 'sala_do_empreendedor/pdde/index_empresa.html', cotext)

@login_required()
def pdde_index_empresa_detalhe_solicitacao(request, id):
    solicitacao = Solicitacao_de_Compras.objects.get(id=id)
    itens = Item_Solicitacao.objects.filter(solicitacao_de_compra=solicitacao)
    if request.method == 'POST':
        if 'empresa' in request.POST:
            itens_valores=[]
            qnt=0
            for item in itens:
                try:
                    itens_valores.append([item.id, request.POST['proposta-'+str(item.id)]])
                    if request.POST['proposta-'+str(item.id)]!='0,00':
                        qnt+=1
                except:
                    pass
            if itens.count() == len(itens_valores):
                print(request.POST)
                empresa=Empresa.objects.get(id=int(request.POST['empresa']))
                if empresa.user_register == request.user:
                    proposta=Proposta.objects.create(
                        qnt_itens_proposta = qnt,
                        solicitacao_de_compra=solicitacao,
                        empresa=empresa,
                        previsao_entrega = request.POST['dt_previsao']
                    )
                    
                    for item_valor in itens_valores:
                        print(item_valor)
                        preco_=item_valor[1].replace(',', '')
                        preco=preco_.replace('.', '')
                        Proposta_Item.objects.create(
                            proposta=proposta,
                            item_solicitacao=Item_Solicitacao.objects.get(id=int(item_valor[0])),
                            preco = preco
                        )
                    messages.success(request, 'Proposta enviada com sucesso!')
                    return redirect('empreendedor:pdde_empresa')
            else:
                messages.warning(request, 'Preencha todos os campos de proposta corretamente.')
        else:
            messages.warning(request, 'Você precisia de uma empresa para enviar a proposta.')
    cotext = {
            'titulo': 'Sala do Empreendedor - PDDE Proposta',
            'solicitacao': solicitacao,
            'itens': itens,
            'tipo': str(solicitacao.get_tipo_display()).lower(),
            'empresas': Empresa.objects.filter(user_register=request.user)
        }
    return render(request, 'sala_do_empreendedor/pdde/listar_itens_para_empresa.html', cotext)
   
@login_required()
def pdde_criar_escola(request):
    if request.method == 'POST':
        form = Escola_Form(request.POST)
        if form.is_valid():
            escola = form.save(commit=False)
            escola.responsavel = request.user
            escola.user_register = request.user
            escola.save()
            messages.success(request, 'Escola cadastrada com sucesso! Aguarde a validação de nossa equipe.')
            return redirect('empreendedor:pdde_escola')
        else:
            print('Erro ao cadastrar escola:', form.errors)            
    else:
        form = Escola_Form(initial={'responsavel': request.user.id})
    context = {
        'titulo': 'Sala do Empreendedor - PDDE Escola - Nova escola',
        'form': form
    }
    return render(request, 'sala_do_empreendedor/pdde/criar_escola.html', context)

@login_required()
def pdde_editar_escola(request, id):
    escola=Escola.objects.get(id=id)
    if request.method == 'POST':
        form = Escola_Form(request.POST, instance=escola)
        if form.is_valid():
            escola = form.save(commit=False)
            escola.user_register = request.user
            escola.save()
            messages.success(request, 'Escola cadastrada com sucesso!')
            return redirect('empreendedor:pdde_admin')
    else:
        form = Escola_Form(instance=escola)
    context = {
        'titulo': 'Sala do Empreendedor - PDDE Escola - Editar escola',
        'form': form
    }
    return render(request, 'sala_do_empreendedor/pdde/criar_escola.html', context)

@login_required()
def pdde_criar_solicitacao_de_compra(request, id):
    escola=Escola.objects.get(id=id)
    if request.method == 'POST':
        form = Solicitacao_de_Compras_Form(request.POST)
        if form.is_valid():
            solicitacao=form.save()
            solicitacao.escola=escola
            solicitacao.save()
            messages.success(request, 'Solicitação cadastrada com sucesso!')
            return redirect('empreendedor:pdde_criar_item_solicitacao', id=solicitacao.id)
    else:
        form = Solicitacao_de_Compras_Form(initial={'escola': escola.id})
    context = {
        'titulo': 'Sala do Empreendedor - PDDE Escola - Nova solicitação',
        'escola': escola,
        'form': form
    }
    return render(request, 'sala_do_empreendedor/pdde/criar_solitacao_de_compra.html', context)

@login_required()
def pdde_criar_itens_solicitacao(request, id):
    
    solicitacao=Solicitacao_de_Compras.objects.get(id=id)
    if solicitacao.status == '3':
        return redirect('empreendedor:pdde_contratacao', id=solicitacao.id)
    # soma={'menor_valor': 0, 'maior_valor': 0}
    if request.method == 'POST':
        response = PDDE_POST(request, solicitacao)
        if response == 'salvo':
            messages.success(request, 'Solicitação criada/iniciada com sucesso! Aguardando propostas.')
            return redirect('empreendedor:pdde_listar_solicitacoes', id=solicitacao.escola.id)
        elif response == 'escola-inativa':
            messages.warning(request, 'Sua escola ainda não foi aprovada pela equipe da Sala do Empreendedor. Aguarde a aprovação para poder criar solicitações.')
            return redirect('empreendedor:pdde_escola')
        elif response[0] == 'proposta-aceita':
            messages.success(request, 'Proposta aceita com sucesso! Criando contrato...')
            return redirect('empreendedor:pdde_contratacao', id=response[1].id)
        itens=Item_Solicitacao.objects.filter(solicitacao_de_compra=solicitacao)
    # elif solicitacao.status != '0':
        # itens, soma = Item_E_Melhor_Proposta(solicitacao)
        # form = Criar_Item_Solicitacao(initial={'solicitacao_de_compra': solicitacao.id})
    else:
        form = Criar_Item_Solicitacao(initial={'solicitacao_de_compra': solicitacao.id})
        itens=Item_Solicitacao.objects.filter(solicitacao_de_compra=solicitacao)
    
    # soma={
    #         'menor_valor': '{:,.2f}'.format(soma['menor_valor']/100).replace('.', '##').replace(',', '.').replace('##', ','), 
    #         'maior_valor': '{:,.2f}'.format(soma['maior_valor']/100).replace('.', '##').replace(',', '.').replace('##', ',')
    #         }
    context = {
        'titulo': 'Sala do Empreendedor - PDDE Escola - Criar itens',
        'solicitacao': solicitacao,
        'itens': itens,
        'form': form,
        'lista_propostas': Listar_Proposta(id),
        # 'soma': soma
    }
    return render(request, 'sala_do_empreendedor/pdde/criar_itens_solicitacao.html', context)

def pdde_contratacao(request, id):
    contrato = Contrato_de_Servico.objects.filter(id=id)
    context = {
        'contrato': contrato
    }
    return render(request, 'sala_do_empreendedor/pdde/contratacao.html', context)

def listar_proposta_para_o_item(request, id, id_item):
    item = Item_Solicitacao.objects.get(id=id_item)
    propostas = Proposta_Item.objects.filter(item_solicitacao=item).order_by('preco')
    context = {
        'titulo': 'Sala do Empreendedor - PDDE Escola - Propostas',
        'item': item,
        'propostas': propostas,
    }
    return render(request, 'sala_do_empreendedor/pdde/listar_propostas.html', context)

def pdde_criar_itens_solicitacao_fetch(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            solicitacao = Solicitacao_de_Compras.objects.get(id=request.POST.get('solicitacao_de_compra'))
            if request.user == solicitacao.escola.responsavel or request.user.is_staff:
                item = Item_Solicitacao(
                    solicitacao_de_compra=solicitacao,
                    nome=request.POST.get('nome'),  
                    quantidade=request.POST.get('quantidade'),
                    unidade=request.POST.get('unidade'),
                    descricao=request.POST.get('descricao'),
                )
                item.save()
                itens = Item_Solicitacao.objects.filter(solicitacao_de_compra=solicitacao)
                itens_json = []
                for item in itens:
                    itens_json.append({
                        'id': item.id,
                        'nome': item.nome,
                        'quantidade': item.quantidade,
                        'unidade': item.unidade,
                        'descricao': item.descricao,

                    })
                return JsonResponse(itens_json, safe=False)
        return JsonResponse({})
    except Exception as E:
        print(E)
        return JsonResponse({'error': 'Ocorreu um erro no servidor'}, status=500)

def pdde_remover_item_solicitacao_featch(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            item = Item_Solicitacao.objects.get(id=request.POST.get('id'))
            solicitacao = item.solicitacao_de_compra
            if request.user == solicitacao.escola.responsavel or request.user.is_staff:
                item.delete()
                itens = Item_Solicitacao.objects.filter(solicitacao_de_compra=solicitacao)
                itens_json = []
                for item in itens:
                    itens_json.append({
                        'id': item.id,
                        'nome': item.nome,
                        'quantidade': item.quantidade,
                        'unidade': item.unidade,
                        'descricao': item.descricao,

                    })
                return JsonResponse(itens_json, safe=False)
        return JsonResponse({})
    except Exception as E:
        print(E)
        return JsonResponse({'error': 'Ocorreu um erro no servidor'}, status=500)   

@login_required
def pdde_listar_solicitacoes(request, id):
    try:
        escola=Escola.objects.get(id=id)
        if escola.responsavel != request.user or request.user.is_staff == False:
            messages.warning(request, 'Você não possui autorização para acessar essa página!')
            return redirect('empreendedor:pdde_index')
    except:
        messages.warning(request, 'Você não possui autorização para acessar essa página!')
        return redirect('empreendedor:pdde_index')
    solicitacoes=Solicitacao_de_Compras.objects.filter(escola=escola)
    context = {
        'titulo': 'Sala do Empreendedor - PDDE Escola - Listar solicitações',
        'escola': escola,
        'solicitacoes': solicitacoes
    }
    return render(request, 'sala_do_empreendedor/pdde/listar_solicitacoes.html', context)

@login_required
def requerimento_ISSQN(request):
    if request.method == 'POST':
        form = RequerimentoISSQNForm(request.POST)
        documentos_pedido_form = DocumentosPedidoForm(request.POST, request.FILES)
        if form.is_valid() and documentos_pedido_form.is_valid():
            empresa = form.save()
            documentos_pedido = documentos_pedido_form.save(commit=False)
            documentos_pedido.empresa = empresa
            documentos_pedido.save()

    else:
        form = RequerimentoISSQNForm()
        documentos_pedido_form = DocumentosPedidoForm(request.POST, request.FILES)

    context={
        'form': form,
        'documentos_pedido_form': documentos_pedido_form,
        'titulo': 'Requerimento para ISSQN como Sociedade Uniprofissional'
    }
    return render(request, 'sala_do_empreendedor/processos_digitais/uniprofissional/index.html', context)