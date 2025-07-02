from django.shortcuts import render, redirect
from ..models import Empresa, Porte_da_Empresa, Ramo_de_Atuacao, Atividade, Andamento_Processo_Digital, Status_do_processo, Processo_Digital, Processo_Status_Documentos_Anexos, Profissao, RequerimentoISS, RequerimentoISSQN, DocumentosPedido, Agente_Sanitario, Agente_Tributario, Agente_Ambiental, Credito_Facil
from ..forms import FormEmpresa, FormAlterarEmpresa, Criar_Processo_Form, Criar_Andamento_Processo, Criar_Processo_Admin_Form, Profissao_Form, Processo_ISS_Form, Criar_Andamento_Processo_Sanitario,Criar_Andamento_Processo_Ambiental
from django.contrib import messages
from autenticacao.models import Pessoa
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
import json
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
# from secretaria_financas.decorators import funcionario_financas_required, setor_financas_required
from sala_do_empreendedor.functions.email import send_email_for_create_process, send_email_for_att_process
from openpyxl import Workbook

import re
from datetime import datetime

@login_required
@staff_member_required
def export_fornecedores_excel(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('Você não tem acesso a essa rota.')

    wb = Workbook()
    ws = wb.active
    ws.title = "Fornecedores cadastrados PMNF" 


    ws.append(['CNPJ da empresa', 'Nome', 'Telefone', 
               'Email', 'Porte', 'Atividade', 
               'Ramo', 'Outro ramo','Data de cadastro', 'Aceita receber mensagem/noticias?'])


    fornecedores = Empresa.objects.all()

    for fornecedor in fornecedores:
        atividades = ', '.join([atividade.atividade for atividade in fornecedor.atividade.all()])
        ramos = ', '.join([ramo.ramo for ramo in fornecedor.ramo.all()])
        ws.append([fornecedor.cnpj, fornecedor.nome, fornecedor.telefone, fornecedor.email, 
               fornecedor.porte.porte if fornecedor.porte else '', 
               atividades, 
               ramos, fornecedor.outro_ramo,str(fornecedor.dt_register), fornecedor.receber_noticias])

    data = datetime.now().strftime("%Y%m%d")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="fornecedores_pmnf_{data}.xlsx"'
    wb.save(response)

    return response


@login_required
# @funcionario_financas_required
# @staff_member_required
def sala_do_empreendedor_admin(request):
    context = {
        'titulo': 'Sala do Empreendedor',
    }
    agente_tributario_qs = Agente_Tributario.objects.filter(user=request.user, ativo=True)
    agente_sanitario_qs = Agente_Sanitario.objects.filter(user=request.user, ativo=True)
    agente_ambiental_qs = Agente_Ambiental.objects.filter(user=request.user, ativo=True)

    if agente_tributario_qs.exists():
        agente_tributario = agente_tributario_qs.first()
        context['agente_tributario'] = agente_tributario

    elif agente_sanitario_qs.exists():
        agente_sanitario = agente_sanitario_qs.first()
        context['agente_sanitario'] = agente_sanitario
    
    elif agente_ambiental_qs.exists():
        agente_ambiental = agente_ambiental_qs.first()
        context['agente_ambiental'] = agente_ambiental

    return render(request, 'sala_do_empreendedor/admin/index.html', context)

@login_required()
def processo_sanitario(request):
    try:
        agente_sanitario = Agente_Sanitario.objects.get(user = request.user, ativo=True)
    except:
        return HttpResponseForbidden('Você não tem permissão para acessar essa página.')
    
    requerimentos_1 = RequerimentoISS.objects.filter(profissao__licenca_sanitaria = True).exclude(processo__status='cn')
    requerimentos_2 = RequerimentoISS.objects.filter(profissao__licenca_sanitaria_com_alvara = True, autonomo_localizado = 's').exclude(processo__status='cn')

    requerimentos_unidos = requerimentos_1 | requerimentos_2
    requerimentos_unidos_ordenados = requerimentos_unidos.order_by('id')
    processos=[]
    for r in requerimentos_unidos_ordenados:
        processos.append(r.processo)
    print(processos, 'opa')
    paginator = Paginator(processos, 50)
    context = {
        'titulo': 'Sala do Empreendedor',
        'processos': paginator.get_page(request.GET.get('page')),
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/index.html', context)

@login_required()
def processo_ambiental(request):
    try:
        agente_ambiental= Agente_Ambiental.objects.get(user = request.user, ativo=True)
    except:
        return HttpResponseForbidden('Você não tem permissão para acessar essa página.')
    
    requerimentos = RequerimentoISS.objects.filter(profissao__licenca_ambiental = True).exclude(processo__status='cn')

    
    
    processos=[]
    for r in requerimentos:
        processos.append(r.processo)
        
    paginator = Paginator(processos, 50)
    context = {
        'titulo': 'Sala do Empreendedor',
        'processos': paginator.get_page(request.GET.get('page')),
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/index.html', context)


@login_required()
def processos_concluidos_sanitario(request):
    try:
        agente_sanitario = Agente_Sanitario.objects.get(user = request.user, ativo=True)
    except:
        return HttpResponseForbidden('Você não tem permissão para acessar essa página.')
    
    requerimentos_1 = RequerimentoISS.objects.filter(processo__status = 'cn', profissao__licenca_sanitaria = True)
    requerimentos_2 = RequerimentoISS.objects.filter(processo__status = 'cn', profissao__licenca_sanitaria_com_alvara = True, autonomo_localizado = 's')

    requerimentos_unidos = requerimentos_1 | requerimentos_2
    requerimentos_unidos_ordenados = requerimentos_unidos.order_by('id')
    processos=[]
    for r in requerimentos_unidos_ordenados:        
        processos.append(r.processo)
    print(processos, 'opa')
    paginator = Paginator(processos, 50)
    context = {
        'titulo': 'Sala do Empreendedor',
        'processos': paginator.get_page(request.GET.get('page')),
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/concluidos.html', context)


@login_required()
# @funcionario_financas_required
def processos_digitais_admin(request):
    try:
        agente_sanitario = Agente_Sanitario.objects.get(user = request.user, ativo=True)
        return redirect('empreendedor:processo_sanitario')
    except:
        try:
            agente_ambiental = Agente_Ambiental.objects.get(user = request.user, ativo=True)
            return redirect('empreendedor:processo_ambiental')
        except:
            try: 
                agente_tributario = Agente_Tributario.objects.get(user = request.user, ativo=True)
            except:
                return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    proecsesos = Processo_Digital.objects.exclude(status='cn').order_by('-dt_solicitacao')    
    paginator = Paginator(proecsesos, 50)
    context = {
        'titulo': 'Sala do Empreendedor',
        'processos': paginator.get_page(request.GET.get('page')),
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/index.html', context)

@login_required()
def processos_concluidos(request):
    try:
        agente_sanitario = Agente_Sanitario.objects.get(user = request.user, ativo=True)
        return redirect('empreendedor:processos_concluidos_sanitario')
    except:
        try: 
            agente_tributario = Agente_Tributario.objects.get(user = request.user, ativo=True)
        except:
            return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    proecsesos = Processo_Digital.objects.filter(status='cn').order_by('-dt_solicitacao')    
    paginator = Paginator(proecsesos, 50)
    context = {
        'titulo': 'Sala do Empreendedor',
        'processos': paginator.get_page(request.GET.get('page')),
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/concluidos.html', context)


@login_required()
@staff_member_required()
def requerimento_iss_admin(request):
    if request.method == 'POST':
        form = Criar_Processo_Admin_Form(request.POST, request.FILES)
        try:
            pessoa = Pessoa.objects.get(cpf=re.sub(r'[^0-9]', '', request.POST['cpf']))
        except:
            pessoa = None
        print(pessoa)
        if pessoa:            
            if form.is_valid():
                processo = form.save(commit=False)
                processo.tipo_processo = 1
                processo.solicitante = pessoa.user
                processo.save()
                andamento = Andamento_Processo_Digital(
                    processo=processo,              
                    status=Status_do_processo.objects.get(id=1),                     
                    observacao = 'Processo criado pelo servidor. Aguardando avaliação do pedido.',
                    servidor = request.user 
                )
                andamento.save()
                status_documentos = Processo_Status_Documentos_Anexos(
                    processo=processo,
                    rg_status = '0',
                    comprovante_endereco_status = '0',
                    diploma_ou_certificado_status = '0',
                    licenca_sanitaria = '0',
                    espelho_iptu_status = '0'
                    
                )
                status_documentos.save()
                messages.success(request, 'Processo criado com sucesso!')
                return redirect('empreendedor:processos_digitais_admin')
        else:
            messages.error(request, 'Não foi encontrado usuário com esse CPF!')
    else:
        form = Criar_Processo_Admin_Form(initial={'tipo_processo': 1, 'solicitante': request.user.id})
        
    context = {
        'titulo': 'Sala do Empreendedor',
        'form': form
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/cadastro_processo.html', context)

def andamento_processo_iss(request, processo):
    requerimento = RequerimentoISS.objects.get(processo=processo)
    andamentos = Andamento_Processo_Digital.objects.filter(processo=processo).order_by('-id')
    try:
        status_documentos = Processo_Status_Documentos_Anexos.objects.get(processo=processo)
    except:
        messages.warning(request, 'Aguardando contribuinte enviar os devidos documentos!')
        return redirect('empreendedor:processos_digitais_admin')
    context = {
        'titulo': 'Sala do Empreendedor - ADM - ISS',
        'processo': processo,
        'andamentos': andamentos,
        'status_documentos': status_documentos,
        'requerimento': requerimento,
        
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/andamento_processo_iss.html', context)

def andamento_processo_iss_uniprofissional(request, processo):
    requerimento = RequerimentoISSQN.objects.get(processo=processo)
    andamentos = Andamento_Processo_Digital.objects.filter(processo=processo).order_by('-id')
    status_documentos = DocumentosPedido.objects.get(requerimento=requerimento)
    context = {
        'titulo': 'Sala do Empreendedor - ADM - ISS Uniprofissional',
        'processo': processo,
        'andamentos': andamentos,
        'status_documentos': status_documentos,
        'requerimento': requerimento,
        
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/andamento_processo_uniprofissional.html', context)

@login_required()
@staff_member_required()
def andamento_processo_admin(request, id):
    try:
        agente_sanitario = Agente_Sanitario.objects.get(user=request.user, ativo=True)
        return redirect('empreendedor:andamento_processo_sanitario', id=id)
    except:
        try:
            agente_ambiental = Agente_Ambiental.objects.get(user=request.user, ativo=True)
            return redirect('empreendedor:andamento_processo_ambiental', id=id)
        except:
            pass
        pass
    processo = Processo_Digital.objects.get(id=id)
    if processo.tipo_processo.id == 1:
        return andamento_processo_iss(request, processo)
    elif processo.tipo_processo.id == 3:
        return andamento_processo_iss_uniprofissional(request, processo)
    return redirect('empreendedor:processos_digitais_admin')

@login_required
def andamento_processo_sanitario(request, id):
    try:
        agente_sanitario = Agente_Sanitario.objects.get(user=request.user, ativo=True)
    except:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    
    processo = Processo_Digital.objects.get(id=id)
    if processo.tipo_processo.id == 1:
        requerimento = RequerimentoISS.objects.get(processo=processo)
        andamentos = Andamento_Processo_Digital.objects.filter(processo=processo).order_by('-id')
        try:
            status_documentos = Processo_Status_Documentos_Anexos.objects.get(processo=processo)
        except Exception as E:
            print(E)
            messages.warning(request, 'Aguardando contribuinte enviar os devidos documentos!')
            return redirect('empreendedor:processos_digitais_admin')
        context = {
            'titulo': 'Sala do Empreendedor - ADM - ISS',
            'processo': processo,
            'andamentos': andamentos,
            'status_documentos': status_documentos,
            'requerimento': requerimento,
            'pessoa': Pessoa.objects.get(user=processo.solicitante)
            
        }
        return render(request, 'sala_do_empreendedor/admin/processos_digitais/andamento_sanitario_iss.html', context)

    return HttpResponseForbidden("Você não tem permissão para acessar essa página.")
    
@login_required
def andamento_processo_ambiental(request, id):
    try:
        agente_ambiental = Agente_Ambiental.objects.get(user=request.user, ativo=True)
    except:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    
    processo = Processo_Digital.objects.get(id=id)
    if processo.tipo_processo.id == 1:
        requerimento = RequerimentoISS.objects.get(processo=processo)
        andamentos = Andamento_Processo_Digital.objects.filter(processo=processo).order_by('-id')
        try:
            status_documentos = Processo_Status_Documentos_Anexos.objects.get(processo=processo)
        except Exception as E:
            print(E)
            messages.warning(request, 'Aguardando contribuinte enviar os devidos documentos!')
            return redirect('empreendedor:processos_digitais_admin')
        context = {
            'titulo': 'Sala do Empreendedor - ADM - ISS',
            'processo': processo,
            'andamentos': andamentos,
            'status_documentos': status_documentos,
            'requerimento': requerimento,
            'pessoa': Pessoa.objects.get(user=processo.solicitante)
            
        }
        return render(request, 'sala_do_empreendedor/admin/processos_digitais/andamento_ambiental_iss.html', context)

    return HttpResponseForbidden("Você não tem permissão para acessar essa página.")
    
     

@login_required()
@staff_member_required()
def novo_andamento_processo(request, id):
    processo = Processo_Digital.objects.get(id=id)
    if processo.tipo_processo.id == 1:
        requerimento = RequerimentoISS.objects.get(processo=processo)
    elif processo.tipo_processo.id == 3:
        requerimento = RequerimentoISSQN.objects.get(processo=processo)
    if request.method == 'POST':
        if request.POST['status'] == 'bg' or request.POST['status'] == 'cn':
            requerimento.boleto = request.FILES['boleto']
            if processo.tipo_processo.id == 1:
                requerimento.n_inscricao = request.POST['inscricao']
        form = Criar_Andamento_Processo(request.POST)
        if form.is_valid():
            andamento = form.save(commit=False)
            andamento.processo = processo
            andamento.servidor = request.user
            andamento.save()
            processo.status = andamento.status
            processo.save() 
            requerimento.save()
            messages.success(request, 'Andamento cadastrado com sucesso!')
            send_email_for_att_process(processo, andamento)
            return redirect('empreendedor:andamento_processo_admin', id)
        else:
            print(form.errors)
    else:
        form = Criar_Andamento_Processo(initial={'processo': processo})
        form_req = Processo_ISS_Form()
    context = {
        'titulo': 'Sala do Empreendedor',
        'processo': processo,
        'form': form,
        'form_req': form_req,
        
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/andamento_processo_novo.html', context)

@login_required()
@staff_member_required()
def novo_andamento_processo_sanitario(request, id):
    processo = Processo_Digital.objects.get(id=id)
    if processo.tipo_processo.id == 1:
        requerimento = RequerimentoISS.objects.get(processo=processo)
    elif processo.tipo_processo.id == 3:
        requerimento = RequerimentoISSQN.objects.get(processo=processo)
    if request.method == 'POST':        
        if request.POST['status'] == 'bs' or request.POST['status'] == 'cn':
            requerimento.boleto = request.FILES['boleto']                        
        form = Criar_Andamento_Processo_Sanitario(request.POST)
        if form.is_valid():
            andamento = form.save(commit=False)
            andamento.processo = processo
            andamento.servidor = request.user
            if 'licensa_sanitaria' in request.FILES:
                documentos= Processo_Status_Documentos_Anexos.objects.get(processo=processo)
                try:
                    documentos.licenca_sanitaria = request.FILES['licensa_sanitaria']
                    documentos.save()
                except:
                    messages.error(request, 'Error ao enviar o documento. TENTE NOVAMENTE. O nome do arquivo anexado não deve conter acentos, cedilha ou caracteres especiais. Exemplo: ç, á, é, ã, õ, ô, ì, ò, ë, ù, ï, ü, etc.')
            if andamento.status == 'ls' or 'se':
                requerimento.boleto_saude_status = True
            andamento.save()
            processo.status = andamento.status
            processo.save() 
            requerimento.save()
            messages.success(request, 'Andamento cadastrado com sucesso!')            
            send_email_for_att_process(processo, andamento)
            return redirect('empreendedor:andamento_processo_admin', id)
        else:
            print(form.errors)
    else:
        form = Criar_Andamento_Processo_Sanitario(initial={'processo': processo, 'observacao': 'Andamento realizado pela Vigilância Sanitária.'})
        form_req = Processo_ISS_Form()
    
    context = {
        'titulo': 'Sala do Empreendedor',
        'processo': processo,
        'form': form,
        'form_req': form_req,
        'processo_sanitario': True,
        
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/andamento_processo_sanitario.html', context)

@login_required()
@staff_member_required()
def novo_andamento_processo_ambiental(request, id):
    processo = Processo_Digital.objects.get(id=id)
    if processo.tipo_processo.id == 1:
        requerimento = RequerimentoISS.objects.get(processo=processo)
    elif processo.tipo_processo.id == 3:
        requerimento = RequerimentoISSQN.objects.get(processo=processo)
    if request.method == 'POST':        
        if request.POST['status'] == 'ba' or request.POST['status'] == 'cn':
            requerimento.boleto = request.FILES['boleto']                    
        form = Criar_Andamento_Processo_Ambiental(request.POST)
        if form.is_valid():
            andamento = form.save(commit=False)
            andamento.processo = processo
            andamento.servidor = request.user
            if 'licensa_sanitaria' in request.FILES:
                documentos= Processo_Status_Documentos_Anexos.objects.get(processo=processo)
                try:
                    documentos.licenca_ambiental = request.FILES['licensa_ambiental']
                    documentos.save()
                except:
                    messages.error(request, 'Error ao enviar o documento. TENTE NOVAMENTE. O nome do arquivo anexado não deve conter acentos, cedilha ou caracteres especiais. Exemplo: ç, á, é, ã, õ, ô, ì, ò, ë, ù, ï, ü, etc.')
            if andamento.status == 'ls' or 'se':
                requerimento.boleto_saude_status = True
            andamento.save()
            processo.status = andamento.status
            processo.save() 
            requerimento.save()
            messages.success(request, 'Andamento cadastrado com sucesso!')            
            send_email_for_att_process(processo, andamento)
            return redirect('empreendedor:andamento_processo_admin', id)
        else:
            print(form.errors)
    else:
        form = Criar_Andamento_Processo_Ambiental(initial={'processo': processo, 'observacao': 'Andamento realizado pelo Meio Ambiente.'})
        form_req = Processo_ISS_Form()
    context = {
        'titulo': 'Sala do Empreendedor',
        'processo': processo,
        'form': form,
        'form_req': form_req,
        'processo_sanitario': True,
        
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/andamento_processo_ambiental.html', context)

@login_required()
@staff_member_required()
def mudaStatus(request):    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        query = data.get('query')
        status_documentos = Processo_Status_Documentos_Anexos.objects.get(id=id)
        setattr(status_documentos, query+'_status', str(data.get('status')))
        status_documentos.save()
        return JsonResponse({'status': 'ok'})            
    return JsonResponse({})

@login_required()
@staff_member_required()
def mudaStatus_ISS(request):    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        query = data.get('query')
        status_documentos = DocumentosPedido.objects.get(id=id)
        setattr(status_documentos, query+'_status', str(data.get('status')))
        status_documentos.save()
        return JsonResponse({'status': 'ok'})            
    return JsonResponse({})

@login_required()
@staff_member_required()
def mudaStatusRG(request):    
    try:
        agente = Agente_Tributario.objects.get(user=request.user, ativo=True)
    except:
        return JsonResponse({})
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        status_documentos = Processo_Status_Documentos_Anexos.objects.get(id=id)
        status_documentos.rg_status = data.get('status')
        status_documentos.agente_att_rg = agente
        status_documentos.save()
        return JsonResponse({'status': 'ok'})            
    return JsonResponse({})

@login_required()
@staff_member_required()
def mudaStatusComprovante(request):
    try:
        agente = Agente_Tributario.objects.get(user=request.user, ativo=True)
    except:
        return JsonResponse({})    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        status_documentos = Processo_Status_Documentos_Anexos.objects.get(id=id)
        status_documentos.comprovante_endereco_status = data.get('status')
        status_documentos.agente_att_endereco = agente
        status_documentos.save()
        return JsonResponse({'status': 'ok'})            
    return JsonResponse({})

@login_required()
@staff_member_required()
def mudaStatusCertificado(request):    
    try:
        agente = Agente_Tributario.objects.get(user=request.user, ativo=True)
    except:
        return JsonResponse({})
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        status_documentos = Processo_Status_Documentos_Anexos.objects.get(id=id)
        status_documentos.diploma_ou_certificado_status = data.get('status')
        status_documentos.agente_att_certificado = agente
        status_documentos.save()
        return JsonResponse({'status': 'ok'})            
    return JsonResponse({})

@login_required()
@staff_member_required()
def mudaStatusLicenca(request):    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        status_documentos = Processo_Status_Documentos_Anexos.objects.get(id=id)
        status_documentos.licenca_sanitaria = data.get('status')
        status_documentos.save()
        return JsonResponse({'status': 'ok'})            
    return JsonResponse({})

@login_required()
@staff_member_required()
def mudaStatusLicencaComTipo(request, tipo):
    try:
        agente = Agente_Sanitario.objects.get(user = request.user)    
    except:
        return JsonResponse({})
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        status_documentos = Processo_Status_Documentos_Anexos.objects.get(id=id)
        status = data.get('status')
        print(tipo, status)
        if tipo == 'caixa':
            status_documentos.comprovante_limpeza_caixa_dagua_status=status
            status_documentos.agente_att_caixa_dagua = agente
        elif tipo == 'ar':
            status_documentos.comprovante_ar_condicionado_status=status
            status_documentos.agente_att_ar  = agente
        elif tipo == 'residuos':
            status_documentos.plano_gerenciamento_de_residuos_status=status
            status_documentos.agente_att_residuos = agente
        elif tipo == 'anterior':
            status_documentos.licenca_santinaria_anterior_status=status
            status_documentos.agente_att_licenca_sanitaria_anterior = agente
        status_documentos.save()
        return JsonResponse({'status': 'ok'})            
    return JsonResponse({})

@login_required()
@staff_member_required()
def mudaStatusEspelho(request):    
    try:
        agente = Agente_Tributario.objects.get(user=request.user, ativo=True)
    except:
        return JsonResponse({})
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        status_documentos = Processo_Status_Documentos_Anexos.objects.get(id=id)
        status_documentos.espelho_iptu_status = data.get('status')
        status_documentos.agente_att_iptu = agente
        status_documentos.save()
        return JsonResponse({'status': 'ok'})            
    return JsonResponse({})

@login_required()
@staff_member_required()
def mapeamento_empresa_e_fornecedores(request):
    empresas=Empresa.objects.all()
    if request.method == 'POST':
        if request.POST['cnpj']!='':
            empresas=empresas.filter(cnpj__icontains=request.POST['cnpj'])
        if request.POST['nome']!='':
            empresas=empresas.filter(nome__icontains=request.POST['nome'])
        if request.POST['porte']!='':
            empresas=empresas.filter(porte__porte__icontains=request.POST['porte'])
        if request.POST['atividade']!='':
            empresas=empresas.filter(atividade__atividade__icontains=request.POST['atividade'])
        if request.POST['ramo']!='':
            empresas=empresas.filter(ramo__ramo__icontains=request.POST['ramo'])
       
    paginator = Paginator(empresas, 100)
    context = {
        'titulo': 'Sala do Empreendedor',
        'portes': Porte_da_Empresa.objects.all(),
        'atividades': Atividade.objects.all(),
        'ramos': Ramo_de_Atuacao.objects.all(),
        'empresas': paginator.get_page(request.GET.get('page')),
        'paginator': paginator,
    }
    return render(request, 'sala_do_empreendedor/admin/mapeamento_empresa_e_fornecedores.html', context)

@login_required()
@staff_member_required()
def cadastrar_profissao(request):
    if request.method == 'POST':
        form = Profissao_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profissão cadastrada com sucesso!')
            return redirect('empreendedor:cadastrar_profissao')
    else:
        form = Profissao_Form()
    context = {
        'titulo': 'Sala do Empreendedor',
        'form': form
    }
    return render(request, 'sala_do_empreendedor/admin/processos_digitais/cadastro_profissao.html', context)