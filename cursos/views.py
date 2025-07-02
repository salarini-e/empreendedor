from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from autenticacao.functions import aluno_required
from .models import *
from .forms import *
from datetime import date, datetime

from .models import *
from .forms import *
from autenticacao.forms import Form_Pessoa, Form_Alterar_Pessoa
from django.apps import apps
from random import shuffle

from desenvolve_nf.models import ClimaTempo
from .functions import ClimaTempoTemperaturas

from django.urls import reverse

def index(request):

    eventos=[]
    
    cursos = list(Curso.objects.filter(tipo='C', ativo=True).order_by('?')[:9])
    palestras = list(Curso.objects.filter(tipo='P', ativo=True).order_by('?')[:4])
    shuffle(cursos)
    context = { 
        'titulo': apps.get_app_config('cursos').verbose_name +' - Página Inicial',
        'eventos': eventos,
        'cursos': cursos,   
        'cursos_en': Curso_Ensino_Superior.objects.all()[:4],
        'palestras': palestras 
    }

    return render(request, 'cursos/index.html', context)


def cidade_inteligente_home(request):
    clima = ClimaTempo.objects.first()
    context = {
        'titulo': 'Ciência e Tecnologia - Cidade Inteligente',
        'clima': clima
    }
    return render(request, 'cidade_inteligente.html', context)

@login_required
def cidade_inteligente_cadastro_camera(request):
    clima = ClimaTempo.objects.first()
    if request.method == 'POST':
        form = Solicitacao_de_cadastro_de_cameraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitação de cadastro de câmera enviada com sucesso!')
            return redirect('cidade_inteligente_cadastro_camera')
    else:
        pessoa = Pessoa.objects.get(user=request.user)
        form = Solicitacao_de_cadastro_de_cameraForm(initial={'pessoa': pessoa})
    context = {
        'titulo': 'Ciência e Tecnologia - Cidade Inteligente',
        'clima': clima,
        'form': form
    }
    return render(request, 'cadastro_camera.html', context)

def cursos(request):
    form = Aluno_form()
    categorias = Categoria.objects.all()
    
    cursos=Curso.objects.filter(tipo='C', ativo=True)

    context = {
        'categorias':categorias,
        'cursos': cursos,
        'form': form,
        'titulo': apps.get_app_config('cursos').verbose_name + ' - ' + 'Cursos',        
        'tipo':'cursos'
    }
    return render(request, 'cursos/cursos.html', context)


def cursos_cevest(request):
    form = Aluno_form()
    categorias = Categoria.objects.all()

    cursos=Curso.objects.filter(tipo='C', categoria__nome='CEVEST', ativo=True)    

    context = {
        'categorias':categorias,
        'cursos': cursos,
        'form': form,
        'titulo': apps.get_app_config('cursos').verbose_name + ' - ' + 'CEVEST',        
        'tipo': 'cevest'
    }
    
    return render(request, 'cursos/cursos.html', context)

def cursos_filtrado(request, tipo, filtro):
    form = Aluno_form()
    categorias = Categoria.objects.all()
    cursos = []
    if tipo == 'cursos':       
       cursos=Curso.objects.filter(tipo='C', categoria__nome=filtro, ativo=True)
    elif tipo == 'palestras':                
        cursos=Curso.objects.filter(tipo='P', categoria__nome=filtro, ativo=True)

    context = {
        'categorias': categorias,
        'cursos': cursos,
        'form': form,
        'titulo': apps.get_app_config('cursos').verbose_name + ' - ' + tipo.capitalize(), 
        'filtro': filtro,
        'tipo': tipo
    }
    if tipo == 'cursos':
        return render(request, 'cursos/cursos.html', context)
    elif tipo == 'palestras':  
        return render(request, 'cursos/palestras.html', context)
    raise Http404("Página não encontrada")

def curso_detalhe(request, tipo, id):    
    curso=Curso.objects.get(id=id)    
    context={
        'curso': curso,
        'tipo': tipo,
        'titulo': apps.get_app_config('cursos').verbose_name+' - Detalhes',
        'turmas': Turma.objects.filter(curso=curso)
    }
    return render(request, 'cursos/curso_detalhe.html', context)

@login_required
def candidatar(request, id):

    curso = Curso.objects.get(id=id)
    form = Aluno_form(initial={'curso': curso})
    if request.method == 'POST':
        form = Aluno_form(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
        'titulo': apps.get_app_config('cursos').verbose_name + ' - Inscrição - ' + curso.nome,
    }
    return render(request, 'cursos/cadastrar_candidato.html', context)


def prematricula(request):
    form = Aluno_form(prefix="candidato")
    form_responsavel = CadastroResponsavelForm(prefix="responsavel")

    categorias = Categoria.objects.all()
    cursos = []

    for i in categorias:
        cursos.append(
            {'categoria': i, 'curso': Curso.objects.filter(categoria=i, ativo=True)})

    if request.method == 'POST':
        dtnascimento_cp = request.POST.get("candidato-dt_nascimento")
        form = Aluno_form(request.POST, prefix="candidato")
        form_responsavel = CadastroResponsavelForm(
            request.POST, prefix="responsavel")

        try:
            dtnascimento_hr = datetime.strptime(dtnascimento_cp, "%d-%m-%Y")
        except:
            dtnascimento_hr = datetime.strptime(dtnascimento_cp, "%Y-%m-%d")

        dt_nascimento = dtnascimento_hr.date()

        today = date.today()
        age = today.year - dt_nascimento.year - \
            ((today.month, today.day) < (dt_nascimento.month, dt_nascimento.day))
        teste = True
        candidato = False

        try:
            cpf = request.POST['cpf']
            candidato = Aluno.objects.get(cpf=cpf)
        except Exception as e:
            pass

        if candidato:        
            turma = Turma.objects.get(id=i)
            if candidato:
                try:
                    Matricula.objects.get(
                        candidato=candidato, turma__curso=turma.curso)
                    messages.error(
                        request, 'Candidato já matriculado no curso ' + turma.curso.nome)
                    return redirect('cursos:curso_detalhe')
                except:
                    pass

            if (turma.idade_minima is not None and age < turma.idade_minima) or (turma.idade_maxima is not None and age > turma.idade_maxima):
                teste = False

        if form.is_valid() and teste:
            candidato = form.save(commit=False)

            if age < 18:

                if form_responsavel.is_valid():

                    responsavel = form_responsavel.save(commit=False)
                    responsavel.aluno = candidato

                else:
                    return redirect('cursos:curso_detalhe')

                responsavel.save()
                candidato.save()

            else:

                candidato.save()

            for i in request.POST.getlist('turmas'):
                Matricula.objects.create(
                    aluno=candidato, turma=turma, status='c')

            messages.success(
                request, 'Pré-inscrição realizada com sucesso! Aguarde nosso contato para finalizar inscrição.')
            return redirect('/')
        else:
            if not teste:
                messages.error(
                    request, 'Não foi possível realizar a inscrição na turma: A idade não atende a faixa etária da turma.')
                return redirect('/prematricula')

    context = {
        'form': form,
        'form_responsavel': form_responsavel,
        'categorias': cursos,
        'titulo': apps.get_app_config('cursos').verbose_name + ' - 001',
    }
    return render(request, 'cursos/pre_matricula.html', context)

def alterarCad(request):
    return render(request, 'cursos/alterar_cad.html')


def resultado(request):
    return render(request, 'cursos/resultado.html')

@login_required
def matricular(request, tipo, id):
    curso=Curso.objects.get(id=id)
    pessoa=Pessoa.objects.get(user=request.user)

    #checa se já é aluno para por informações no formulario
    try:
        aluno=Aluno.objects.get(pessoa=pessoa)
        form = Aluno_form(prefix="candidato", instance=aluno)
        try:            
            form_responsavel = CadastroResponsavelForm(prefix="responsavel", instance=aluno)
        except:
            pass
    except Exception as E:        
        aluno=None     
        form = Aluno_form(prefix="candidato")    
        form_responsavel = CadastroResponsavelForm(prefix="responsavel")

    # Checa a idade e se precisa de responsavel
    dtnascimento = pessoa.dt_nascimento    
    today = date.today()
    age = today.year - dtnascimento.year - \
            ((today.month, today.day) < (dtnascimento.month, dtnascimento.day))    
    # precisa_responsavel=age<18
    precisa_responsavel=False
    
    if request.method == 'POST':
        
        form = Aluno_form(request.POST, prefix="candidato", instance=aluno)
        if precisa_responsavel:
            form_responsavel = CadastroResponsavelForm(
                request.POST, prefix="responsavel", instance=aluno)

        
        teste = True        
        
        candidato = aluno
        

        #checando idade minima e maxima para o curso
        turmas=Turma.objects.filter(curso=curso)
        pode_cursar=True
        if len(turmas)!=0:
            for turma in turmas:
                if (turma.idade_minima is not None and age < turma.idade_minima) or (turma.idade_maxima is not None and age > turma.idade_maxima):
                    teste = False
                    if not teste:
                        print('entrou aqui')
                        pode_cursar=False
                        teste=True
            
        #validação das informações do forms
        if form.is_valid() and pode_cursar:
            if candidato:
                for turma in turmas:
                    try:
                        Matricula.objects.get(
                            aluno=candidato, turma__curso=turma.curso)
                        messages.error(
                            request, 'Candidato já matriculado no curso: ' + turma.curso.nome)
                        return redirect(reverse('cursos:curso_detalhe', args=[tipo, id]))
                    except Exception as E:                        
                        pass
            candidato = form.save(commit=False)

            if precisa_responsavel:
                if form_responsavel.is_valid():
                    responsavel = form_responsavel.save(commit=False)
                    responsavel.aluno = candidato
                else:       
                    messages.warning(
                    request, 'Preencha corretamente os campos do formulário!')
                    context = {
                        'age': age,
                        'form': form,
                        'form_responsavel': form_responsavel,     
                        'titulo': apps.get_app_config('cursos').verbose_name+' - Inscrever-se',
                        'curso': curso,
                        'pessoa': pessoa
                    }             
                    return render(request, 'cursos/pre_matricula.html', context)
                candidato.pessoa=pessoa
                candidato.save()                                
                responsavel.save()
                
            else:
                candidato.pessoa=pessoa
                # candidato.disponibilidade.clear()
                # for i in request.POST.getlist('candidato-disponibilidade'):
                #     disponibilidade=Disponibilidade.objects.get(id=i)
                #     candidato.disponibilidade.add(disponibilidade)                    
                candidato.save()                    
                # print('ops')
                

            #criando matricula como candidato na turma
            try:
                turma=Turma.objects.filter(curso=curso, status='pre')
                turma_disponibilidade =[]
                # candidato_disponibilidade=[]
                # for i in turma.disponibilidade.all():
                #         turma_disponibilidade.append(i.disponibilidade)
                # for i in candidato.disponibilidade.all():
                #         candidato_disponibilidade.append(i.disponibilidade)
                # pode_entrar = any(disponibilidade in turma_disponibilidade for disponibilidade in candidato_disponibilidade)
                # if pode_entrar:
                Matricula.objects.create(
                        aluno=candidato, turma=turma[0], status='c')
                # else:
                #     messages.error(
                #     request, 'Não foi possível realizar a matricula na turma, pois sua disponibilidade não é compátivel com o da turma aberta.')
                #     context = {
                #             'age': age,
                #             'form': form,
                #             'form_responsavel': form_responsavel,     
                #             'titulo': apps.get_app_config('cursos').verbose_name,
                #             'curso': curso,
                #             'pessoa': pessoa
                #         }
                #     return render(request, 'cursos/pre_matricula.html', context)
            except:     
                try:
                    turma=Turma.objects.filter(curso=curso, status='acc')
                    # turma_disponibilidade=[]
                    # candidato_disponibilidade=[]
                    # for i in turma.disponibilidade.all():
                    #         turma_disponibilidade.append(i.disponibilidade)
                    # for i in candidato.disponibilidade.all():
                    #         candidato_disponibilidade.append(i.disponibilidade)
                    # pode_entrar = any(disponibilidade in turma_disponibilidade for disponibilidade in candidato_disponibilidade)
                    # if pode_entrar:
                    Matricula.objects.create(
                            aluno=candidato, turma=turma[0], status='c')
                    # else:
                    #     messages.error(
                    #     request, 'Não foi possível realizar a matricula na turma, pois sua disponibilidade não é compátivel com o da turma aberta.')
                    #     context = {
                    #         'age': age,
                    #         'form': form,
                    #         'form_responsavel': form_responsavel,     
                    #         'titulo': apps.get_app_config('cursos').verbose_name,
                    #         'curso': curso,
                    #         'pessoa': pessoa
                    #     }
                    #     return render(request, 'cursos/pre_matricula.html', context)
                except:
                    # pode_entrar=False
                    Alertar_Aluno_Sobre_Nova_Turma.objects.create(
                        aluno=candidato,
                        curso=curso
                    )
                    messages.success(request, 'Você será informado quando abrir o a inscrição de uma nova turma para este curso!')
                    return redirect(reverse('cursos:matricula', args=[tipo,id]))
            
            messages.success(
                request, 'Pré-inscrição realizada com sucesso! Aguarde nosso contato para finalizar inscrição.')
            print('passou aqui 2')
            return redirect(reverse('cursos:curso_detalhe', args=[tipo, id]))
        else:
            print('passou aqui')
            if not teste:
                messages.error(
                    request, 'Não foi possível realizar a inscrição na turma: A idade não atende a faixa etária da turma.')
                return redirect(reverse('cursos:curso_detalhe', args=[tipo, id]))

    context = {
        'age': age,
        'form': form,
        'form_responsavel': form_responsavel,     
        'titulo': apps.get_app_config('cursos').verbose_name+' - Inscrever-se',
        'curso': curso,
        'pessoa': pessoa
    }
    return render(request, 'cursos/pre_matricula.html', context)

from django.http import HttpResponse
from openpyxl import Workbook

def exportar_para_excel(request):
    # Filtrar as turmas com status 'pre'
    cursos = Curso.objects.all().order_by('nome')
    
    # Criar um workbook do Excel
    wb = Workbook()
    # Criar uma planilha
    ws = wb.active
    ws.title = "Alunos Interessados"
    
    # Adicionar cabeçalho à planilha
    ws.append(["Curso", "Aluno", "Envio do pedido", "Telefone", "Email"])

    # Iterar sobre as turmas
    for curso in cursos:
        # Filtrar os alertas para esta turma e após a data de inclusão da turma
        alertas = Alertar_Aluno_Sobre_Nova_Turma.objects.filter(curso=curso, alertado=False)
        # Adicionar os alunos alertados à planilha
        for alerta in alertas:
            ws.append([curso.nome, alerta.aluno.pessoa.nome, alerta.dt_inclusao, alerta.aluno.pessoa.telefone, alerta.aluno.pessoa.email ]) 

    # Definir o nome do arquivo
    dataHora = datetime.datetime.now()
    dataHora_formatada = dataHora.strftime("%Y%m%d_%H%M%S")
    file_name = f"alunos_interessados_{dataHora_formatada}.xlsx"
    
    # Criar uma resposta HTTP para o arquivo Excel
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = f"attachment; filename={file_name}"
    
    # Salvar o workbook e escrever na resposta HTTP
    wb.save(response)

    return response

def exportar_para_excel_por_turma(request):
    # Filtrar os cursos, excluindo o CEVEST
    # cursos = Curso.objects.exclude(categoria__nome='CEVEST')
    cursos = Curso.objects.all()

    # Criar um novo arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Alunos por Curso"

    # Adicionar cabeçalhos
    ws.append(['Curso', 'Aluno', 'Email', 'Telefone', 'Status da Matrícula'])

    # Iterar sobre os cursos
    for curso in cursos:
        # Filtrar matrículas por curso
        matriculas = Matricula.objects.filter(turma__curso=curso)

        # Iterar sobre as matrículas
        for matricula in matriculas:
            # Adicionar detalhes do aluno e da matrícula ao Excel
            ws.append([curso.nome, matricula.aluno.pessoa.nome, matricula.aluno.pessoa.email, matricula.aluno.pessoa.telefone, matricula.get_status_display()])

    # Criar a resposta do HTTP com o conteúdo do arquivo Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=alunos_por_curso.xlsx'
    wb.save(response)

    return response

def ensino_superior(request):
    context = {
        'titulo': apps.get_app_config('cursos').verbose_name+' - Ensino Superior',
        'cursos': Curso_Ensino_Superior.objects.all()
    }
    return render(request, 'cursos/ensino_superior.html', context)

# def ensino_superior_detalhe(request, id):    
#     curso=Curso.objects.get(id=id)
#     context={
#         'curso': curso,
#         'tipo': tipo,
#         'titulo': apps.get_app_config('cursos').verbose_name,
#         'turmas': Turma.objects.filter(curso=curso)
#     }
#     return render(request, 'cursos/curso_detalhe.html', context)

def ensino_tecnico(request):
    context = {
        'titulo': apps.get_app_config('cursos').verbose_name+' - Ensino Técnico',
        # 'cursos': Curso_Ensino_Superior.objects.all()
    }
    return render(request, 'cursos/ensino_tecnico.html', context)

def curriculo_vitae(request):
    context = {
        'titulo': apps.get_app_config('cursos').verbose_name+' - Currículo Vitae',
    }
    return render(request, 'cursos/curriculo_vitae.html', context)

def area_do_estudante(request):
    pessoa=Pessoa.objects.get(user=request.user)
    try:
        aluno=Aluno.objects.get(pessoa=pessoa)
    except:
        messages.error(request, 'Você não é um aluno! Primeiro você deve se inscrever em um curso.')
        return redirect('cursos:cursos', tipo='cursos')
    matriculas=Matricula.objects.filter(aluno=aluno).order_by('-turma__data_inicio')
    alertas=Alertar_Aluno_Sobre_Nova_Turma.objects.filter(aluno=aluno, alertado=False).order_by('-dt_inclusao')
    context={
        'matriculas': matriculas,
        'alertas': alertas,
        'titulo': apps.get_app_config('cursos').verbose_name+' - Área do Estudante'
    }
    return render(request, 'cursos/area_do_estudante.html', context)

def editar_cadastro(request):    
    pessoa=Pessoa.objects.get(user=request.user)
    form_pessoa=Form_Alterar_Pessoa(instance=pessoa)    
    if request.method == 'POST':
        form_pessoa=Form_Alterar_Pessoa(request.POST, instance=pessoa)
        if form_pessoa.is_valid:
            form_pessoa.save()
    context={        
        'form_pessoa': form_pessoa,
        'titulo': apps.get_app_config('cursos').verbose_name+' - Editar Cadastro'
    }
    return render(request, 'cursos/editar_cadastro.html', context)

def editar_cadastro_pessoa(request):    
    pessoa=Pessoa.objects.get(user=request.user)
    form_pessoa=Form_Pessoa(instance=pessoa)    
    if request.method == 'POST':
        form_pessoa=Form_Pessoa(request.POST, instance=pessoa)
        if form_pessoa.is_valid:
            form_pessoa.save()
            return redirect('cursos:home')
    context={        
        'form_pessoa': form_pessoa,
        'titulo': apps.get_app_config('cursos').verbose_name+' - Editar Cadastro'
    }
    return render(request, 'cursos/editar_cadastro_pessoa.html', context)

def alterar_senha(request):
    form_user = PasswordChangeCustomForm(user=request.user)

    if request.method == 'POST':
        form_user = PasswordChangeCustomForm(user=request.user, data=request.POST)
        if form_user.is_valid():
            form_user.save()
            return redirect('cursos:home')

    context = {        
        'form_user': form_user,
        'titulo': apps.get_app_config('cursos').verbose_name+' - Alterar Senha'
    }
    return render(request, 'cursos/altera_senha.html', context)