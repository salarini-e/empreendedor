from django.shortcuts import render, redirect, get_object_or_404
from ..models import Empresa
from ..forms import FormEmpresa, FormAlterarEmpresa, Form_Necessidades_das_Empresas
from django.contrib import messages
from autenticacao.models import Pessoa
from django.contrib.auth.decorators import login_required
from ..models import Proposta, Solicitacao_de_Compras, Contrato_de_Servico
# from formularios.models import CadastroPCA
from django.core.paginator import Paginator
from django.db.models import Q
from ..models import Atividade, Porte_da_Empresa, Ramo_de_Atuacao, Registro_no_vitrine_virtual

@login_required()
def minha_empresa(request):
    empresas = Empresa.objects.filter(user_register=request.user)
    contrato = Contrato_de_Servico.objects.filter(proposta_vencedora__empresa__user_register=request.user)
    context = {
        'titulo': 'Sala do Empreendedor - Minha Empresa',
        'empresas': empresas,
        'pdde': contrato,
        'pdde_count': contrato.count(),
    }
    return render(request, 'sala_do_empreendedor/minha-empresa/index.html', context)

import re
@login_required()
def cadastrar_empresa(request):
    
    if request.method == 'POST':
        form = FormEmpresa(request.POST)
        form_necessidades = Form_Necessidades_das_Empresas()
        if form.is_valid():
            empresa=form.save()
            empresa.user_register=request.user
            empresa.cnpj=re.sub(r'[^0-9]', '', empresa.cnpj)
            empresa.save()
            messages.success(request, 'Empresa cadastrada com sucesso!')
            pessoa=Pessoa.objects.get(user=request.user)
            pessoa.possui_cnpj=True
            pessoa.save()
            necessidades = form_necessidades.save()
            necessidades.empresa = empresa
            necessidades.user_register =  request.user
            necessidades.save()
            return redirect('empreendedor:minha_empresa')
        else:
            print('error')
            print(form.errors)
            print(form_necessidades.errors)
    else:
        form=FormEmpresa()
        form_necessidades =  Form_Necessidades_das_Empresas()
    context = {
        'titulo': 'Sala do Empreendedor - Cadastrar Empresa',
        'form': form,
        'form_necessidades': form_necessidades,
    }
    return render(request, 'sala_do_empreendedor/minha-empresa/cadastro_empresa.html', context)

@login_required()
def editar_empresa(request, id):
    instance=Empresa.objects.get(id=id)
    
    if request.user.is_staff or request.user==instance.user_register:
    
        form=FormAlterarEmpresa(instance=instance)
        if request.method == 'POST':
            form = FormAlterarEmpresa(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Informações da empresa atualizada com sucesso!')
                return redirect('empreendedor:minha_empresa')
        context = {
            'empresa': instance,
            'titulo': 'Sala do Empreendedor - Editar Empresa',
            'form': form
        }
        return render(request, 'sala_do_empreendedor/minha-empresa/editar_empresa.html', context)
    return redirect('empreendedor:minha_empresa')

from django.db.models import F, Value
from django.db.models.functions import Substr, Concat
from datetime import datetime

def pca_list(request):
    ano_atual = datetime.now().year
    ano_seguinte_str = str(ano_atual + 1)

    # informacoes_pca = CadastroPCA.objects.filter(
    #     data_prevista_certame__contains=ano_seguinte_str  #Filtra registros que contém o ano seguinte na string
    # ).order_by('data_prevista_certame').values(
    #     data_certame=F('data_prevista_certame'),  #Campo data (mês/ano)
    #     mes_certame=Substr(F('data_prevista_certame'), 1, 2),  #Extraindo o mês
    #     objeto=F('objeto_licitacao'),
    #     orgao_nome=F('orgao_requisitante'),  #Renomeando para evitar conflito
    #     valor_previsto=F('preco_estimado')
    # )
    informacoes_pca = []
    context = {
        'informacoes_pca': informacoes_pca ,
    }
    return render(request, 'sala_do_empreendedor/minha-empresa/pca_list.html', context)

def pca_list_excel_download(request):
    if not request.user.is_staff:
        return redirect('empreendedor:minha_empresa')
    
    from django.http import HttpResponse
    import openpyxl

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="pca_list.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'PCA List'

    #Cabeçalho
    ws.append([
        'Data do Certame',
        'Mês do Certame',
        'Objeto da Licitação',
        'Órgão Requisitante',
        'Valor Previsto'
    ])

    #Dados
    ano_atual = datetime.now().year
    ano_seguinte_str = str(ano_atual + 1)

    # informacoes_pca = CadastroPCA.objects.filter(
    #     data_prevista_certame__contains=ano_seguinte_str  #Filtra registros que contém o ano seguinte na string
    # ).order_by('data_prevista_certame').values(
    #     data_certame=F('data_prevista_certame'),  #Campo data (mês/ano)
    #     mes_certame=Substr(F('data_prevista_certame'), 1, 2),  #Extraindo o mês
    #     objeto=F('objeto_licitacao'),
    #     orgao_nome=F('orgao_requisitante'),  #Renomeando para evitar conflito
    #     valor_previsto=F('preco_estimado')
    # )
    informacoes_pca = []

    for pca in informacoes_pca:
        ws.append([
            pca['data_certame'],
            pca['mes_certame'],
            pca['objeto'],
            pca['orgao_nome'],
            pca['valor_previsto']
        ])

    wb.save(response)
    return response

def perfil_empresa(request, empresa_id):
    """
    View para exibir o perfil completo de uma empresa
    """
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    # Verificar permissões de acesso
    is_owner = request.user.is_authenticated and empresa.user_register == request.user
    is_admin = request.user.is_authenticated and request.user.is_staff
    is_public = empresa.perfil_publico
    
    # Se não é público e o usuário não é dono nem admin, negar acesso
    if not is_public and not is_owner and not is_admin:
        messages.error(request, 'Esta empresa não permite visualização pública do perfil.')
        return redirect('empreendedor:index')
    
    registro = Registro_no_vitrine_virtual.objects.filter(empresa=empresa)
    context = {
        'titulo': f'Perfil - {empresa.nome}',
        'empresa': empresa,
        'is_owner': is_owner,
        'is_admin': is_admin,
        'is_public': is_public,
        'registro_no_vitrine_virtual': registro.first() if registro.exists() else None
    }
    
    return render(request, 'sala_do_empreendedor/minha-empresa/perfil_empresa.html', context)

def pesquisar_empresas(request):
    """
    Lista todas as empresas com filtros avançados (páginas pesquisa_empresa)
    """
    from django.db.models import Q
    from django.core.paginator import Paginator
    from ..models import Atividade, Porte_da_Empresa, Ramo_de_Atuacao
    
    # Buscar apenas empresas validadas e com perfil público
    empresas = Empresa.objects.filter(
        validacao=True, 
        perfil_publico=True
    ).select_related(
        'porte'
    ).prefetch_related('atividade', 'ramo').order_by('nome')
    
    # Aplicar filtros
    nome = request.GET.get('nome', '')
    atividade_id = request.GET.get('atividade', '')
    porte_id = request.GET.get('porte', '')
    ramo_id = request.GET.get('ramo', '')
    tem_website = request.GET.get('tem_website', '')
    
    if nome:
        empresas = empresas.filter(nome__icontains=nome)
    
    if atividade_id:
        empresas = empresas.filter(atividade__id=atividade_id)
    
    if porte_id:
        empresas = empresas.filter(porte_id=porte_id)
    
    if ramo_id:
        empresas = empresas.filter(ramo__id=ramo_id)
    
    if tem_website == 'sim':
        empresas = empresas.exclude(Q(site__isnull=True) | Q(site=''))
    elif tem_website == 'nao':
        empresas = empresas.filter(Q(site__isnull=True) | Q(site=''))
    
    # Paginação
    paginator = Paginator(empresas, 12)  # 12 empresas por página
    page_number = request.GET.get('page')
    empresas_paginadas = paginator.get_page(page_number)
    
    # Dados para os filtros
    atividades = Atividade.objects.all().order_by('atividade')
    portes = Porte_da_Empresa.objects.all().order_by('porte')
    ramos = Ramo_de_Atuacao.objects.all().order_by('ramo')
    
    context = {
        'titulo': 'Pesquisar empresas - Empresas Cadastradas',
        'empresas': empresas_paginadas,
        'atividades': atividades,
        'portes': portes,
        'ramos': ramos,
        'filtros': {
            'nome': nome,
            'atividade': atividade_id,
            'porte': porte_id,
            'ramo': ramo_id,
            'tem_website': tem_website,
        },
        'total_empresas': paginator.count,
    }
    return render(request, 'sala_do_empreendedor/pesquisar_empresas.html', context)