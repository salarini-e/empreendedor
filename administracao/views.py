# from bemestaranimal.models import *
# from bemestaranimal.forms import *
from .functions import generateToken
from django.db import IntegrityError
import unicodedata
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db.models import Q, Count
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from cursos.models import *
from datetime import date
from django.template.loader import render_to_string
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator

from django.contrib.auth.decorators import user_passes_test
from autenticacao.functions import validate_cpf
from autenticacao.forms import Form_Pessoa, Form_Alterar_Pessoa
from django.contrib.auth.decorators import login_required

import csv
import re

from .models import *
from cursos.forms import *

# from eventos.models import *
# from eventos.forms import *

# from palestras.models import *
# from palestras.forms import *


@staff_member_required
def enviar_email(aluno, turma):
    try:
        subject = f'Inscrição no curso {turma.curso.nome}'
        from_email = settings.EMAIL_HOST_USER
        to = [aluno.email]
        text_content = 'This is an important message.'
        html_content = render_to_string('email.html', {
            'turma': turma,
            'aluno': aluno
        }
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as E:
        print(E)
    else:
        print('email enviado com sucesso!')


@staff_member_required
def adm_cursos_cadastrar(request):
    form = CadastroCursoForm()

    if request.method == 'POST':
        form = CadastroCursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.user_inclusao = request.user
            curso.user_ultima_alteracao = request.user
            curso.save()

            messages.success(request, 'Novo curso cadastrado!')
            return redirect('adm_cursos_listar')

    context = {
        'form': form,
        'CADASTRAR': 'NOVO'
    }
    return render(request, 'app_cursos/cursos/adm_cursos_cad_edit.html', context)

@staff_member_required
def adm_curso_visualizar(request, id):
    curso = get_object_or_404(Curso, pk=id)
    turmas = Turma.objects.filter(curso=curso)
    context = {
        'curso': curso,
        'turmas': turmas,
        'CADASTRAR': 'NOVO'
    }
    return render(request, 'app_cursos/cursos/adm_curso_visualizar.html', context)

@staff_member_required
def adm_curso_editar(request, id):
    curso = Curso.objects.get(id=id)
    form = CadastroCursoForm(instance=curso)

    if request.method == 'POST':
        form = CadastroCursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
        'CADASTRAR': 'EDITAR',
        'curso': curso
    }
    return render(request, 'app_cursos/cursos/adm_cursos_cad_edit.html', context)

@staff_member_required
def adm_curso_detalhes(request, id):
    curso = Curso.objects.get(id=id)
    interessados = Alertar_Aluno_Sobre_Nova_Turma.objects.filter(curso=curso, alertado=False).order_by('aluno__pessoa__nome')
    matrizCur = Disciplinas.objects.filter(curso=curso)

    context = {
        'curso': curso,
        'interessados': interessados,
        'matrizesCur': matrizCur
    }
    return render(request, 'app_cursos/cursos/adm_cursos_detalhes.html', context)

# @staff_member_required
# def adm_cadastrar_


@staff_member_required
def cadastrar_categoria(request):

    form = CadastroCategoriaForm()
    if request.method == 'POST':
        form = CadastroCategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova categoria cadastrada!')
            return redirect('adm_categorias_listar')
    context = {
        'form': form
    }
    return render(request, 'app_cursos/cursos/cadastrar_categoria.html', context)

@staff_member_required
def remover_interessado(request, id_curso, id):
    try:
        interessado = Alertar_Aluno_Sobre_Nova_Turma.objects.get(id=id)
        interessado.alertado = True
        interessado.save()
        return JsonResponse({'success': True})  # Retorno de sucesso como JSON
    except Alertar_Aluno_Sobre_Nova_Turma.DoesNotExist:
        return JsonResponse({'success': False})  # Retorno de falha como JSON

@staff_member_required
def cadastrar_local(request):
    form = CadastroLocalForm()

    if request.method == 'POST':
        form = CadastroLocalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo local cadastrado!')
            return redirect('adm_locais_listar')
    context = {
        'form': form
    }
    return render(request, 'app_cursos/cursos/cadastrar_local.html', context)


@staff_member_required
def administrativo(request):
    return render(request, 'administrativo.html')


@staff_member_required
def turmas(request):
    return render(request, 'app_cursos/turmas/adm_turmas.html')


@staff_member_required
def adm_turmas_cadastrar(request):
    form = CadastroTurmaForm()

    if request.method == 'POST':
        form = CadastroTurmaForm(request.POST)
        if form.is_valid():
            turma = form.save(commit=False)
            turma.user_inclusao = request.user
            turma.user_ultima_alteracao = request.user
            turma.save()
            messages.success(request, 'Nova turma cadastrada com sucesso!')
            return redirect('adm_turmas_listar')
    context = {
        'form': form
    }
    return render(request, 'app_cursos/turmas/adm_turmas_cadastrar.html', context)


@staff_member_required
def adm_turmas_listar(request):

    turmas = Turma.objects.exclude(status='enc').order_by('data_final')

    context = {
        'turmas': turmas
    }
    return render(request, 'app_cursos/turmas/adm_turmas_listar.html', context)

@staff_member_required
def adm_turmas_listar_encerradas(request):
    turmas = Turma.objects.filter(status="enc").order_by('-data_final')

    context = {
        'turmas': turmas
    }
    return render(request, 'app_cursos/turmas/adm_turmas_listar_encerradas.html', context)


@staff_member_required
def adm_cursos_listar(request):
    cursos = Curso.objects.all()

    context = {
        'cursos': cursos
    }
    return render(request, 'app_cursos/cursos/adm_cursos_listar.html', context)


@staff_member_required
def adm_locais(request):
    return render(request, 'app_cursos/locais/adm_locais.html')


@staff_member_required
def adm_locais_cadastrar(request):
    form = CadastroLocalForm()
    if request.method == 'POST':
        form = CadastroLocalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo local cadastrado!')
            return redirect('adm_locais_listar')

    context = {
        'form': form,
        'CADASTRAR': 'NOVO'
    }
    return render(request, 'app_cursos/locais/adm_locais_cadastrar.html', context)


@staff_member_required
def adm_locais_listar(request):
    locais = Local.objects.all()
    context = {
        'locais': locais
    }
    return render(request, 'app_cursos/locais/adm_locais_listar.html', context)


@staff_member_required
def adm_locais_editar(request, id):
    local = Local.objects.get(id=id)
    form = CadastroLocalForm(instance=local)
    if request.method == 'POST':
        form = CadastroLocalForm(request.POST, instance=local)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Informações do local atualizada com sucesso')
            return redirect('adm_locais_listar')

    context = {
        'form': form,
        'local': local
    }
    return render(request, 'app_cursos/locais/adm_locais_editar.html', context)


@staff_member_required
def adm_locais_excluir(request, id):
    local = Local.objects.get(id=id)
    local.delete()
    return redirect('adm_locais_listar')


@staff_member_required
def adm_categorias(request):
    return render(request, 'app_cursos/categorias/adm_categorias.html')


@staff_member_required
def adm_categorias_cadastrar(request):
    form = CadastroCategoriaForm()
    if request.method == 'POST':
        form = CadastroCategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova categoria cadastrada!')
            return redirect('adm_categorias_listar')

    context = {
        'form': form,
        'CADASTRAR': 'NOVO'
    }
    return render(request, 'app_cursos/categorias/adm_categorias_cadastrar.html', context)


@staff_member_required
def adm_categorias_listar(request):
    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias
    }
    return render(request, 'app_cursos/categorias/adm_categorias_listar.html', context)


@staff_member_required
def adm_categorias_excluir(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('adm_categorias_listar')


@staff_member_required
def adm_categorias_editar(request, id):
    categoria = Categoria.objects.get(id=id)
    form = CadastroCategoriaForm(instance=categoria)
    if request.method == 'POST':
        form = CadastroCategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informações da categoria atualizada!')
            return redirect('adm_categorias_listar')

    context = {
        'form': form,
        'categoria': categoria
    }
    return render(request, 'app_cursos/categorias/adm_categorias_editar.html', context)


@staff_member_required
def adm_instituicoes_listar(request):
    instituicoes = Instituicao.objects.all()
    context = {
        'instituicoes': instituicoes
    }
    return render(request, 'app_cursos/instituicoes/adm_instituicoes_listar.html', context)


@staff_member_required
def adm_instituicao_cadastrar(request):
    form = Instituicao_form()
    if request.method == 'POST':
        form = Instituicao_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova instituição cadastrada!')
            return redirect('adm_instituicoes_listar')

    context = {
        'form': form,
        'CADASTRAR': 'NOVO'
    }
    return render(request, 'app_cursos/instituicoes/adm_instituicao_cadastrar.html', context)


@staff_member_required
def adm_turno_cadastrar(request, id):

    turma = get_object_or_404(Turma, pk=id)
    form = Turno_form()

    if request.method == 'POST':
        form = Turno_form(request.POST)
        if form.is_valid():
            turno = form.save()

            Turno_estabelecido.objects.create(turno=turno, turma=turma)

            messages.success(request, 'Novo turno cadastrado!')
            return redirect('adm_turma_visualizar', turma.id)

    context = {
        'form': form,
        'CADASTRAR': 'NOVO'
    }
    return render(request, 'app_cursos/turnos/adm_turno_cadastrar.html', context)


@staff_member_required
def adm_professores(request):
    context = {}
    return render(request, 'app_cursos/professores/adm_professores.html', context)


@staff_member_required
def adm_professores_cadastrar(request):
    form = CadastroProfessorForm()
    if request.method == 'POST':
        form = CadastroProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo Instrutor cadastrada com sucesso!')
            return redirect('adm_professores_listar')

    context = {
        'form': form,
    }
    return render(request, 'app_cursos/professores/adm_professores_cadastrar.html', context)


@staff_member_required
def adm_professores_listar(request):
    instrutores = Instrutor.objects.all()
    context = {
        'Instrutores': instrutores
    }
    return render(request, 'app_cursos/professores/adm_professores_listar.html', context)


@staff_member_required
def adm_professores_editar(request, id):
    instrutor = Instrutor.objects.get(id=id)
    form = CadastroProfessorForm(instance=instrutor)
    if request.method == 'POST':
        form = CadastroProfessorForm(request.POST, instance=instrutor)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Informações do Instrutor atualizadas com sucesso!')
            return redirect('adm_professores_Listar')

    context = {
        'form': form,
        'instrutor': instrutor
    }
    return render(request, 'app_cursos/professores/adm_professores_editar.html', context)


@staff_member_required
def adm_professores_excluir(request, id):
    instrutor = Instrutor.objects.get(id=id)
    instrutor.delete()
    return redirect('adm_professores_listar')

@staff_member_required
def gerar_certificados(request, id):
    data_atual = datetime.date.today()
    turma = get_object_or_404(Turma, id=id)
    matriculas=Matricula.objects.filter(turma_id=id)
    disciplinas = Disciplinas.objects.filter(curso_id=turma.curso.id)
    aux=[0,0]
    for d in disciplinas:
        aux[0]+=int(d.n_aulas)
        aux[1]+=int(d.carga_horaria)
    context={
        'turma': turma,
        'matriculas': matriculas,
        'data_atual': data_atual,
        'instrutor': turma.instrutores.all()[0],
        'disciplinas': disciplinas,
        'total_aulas': aux[0],
        'total_horas': aux[1]
    }
    return render(request, 'certificados.html', context)

@staff_member_required
def adm_turmas_visualizar(request, id):
    turma = Turma.objects.get(id=id)

    matriculas = Matricula.objects.filter(turma=turma)

    matriculas_alunos = matriculas.filter(status='a').select_related('aluno')

    total_aulas = Aula.objects.filter(
        associacao_turma_turno__turma=turma).count()

    matriculas_alunos_array = []
    for matricula in matriculas_alunos:
        presencas = Presenca.objects.filter(matricula=matricula.matricula).count()
        frequencia = "Nenhuma aula registrada"
        if total_aulas:
            frequencia = f"{presencas/total_aulas * 100}%"

        matriculas_alunos_array.append(
            {'aluno': matricula.aluno, 'matricula': matricula, 'frequencia': frequencia})

    matriculas_selecionados = matriculas.filter(
        status='s').select_related('aluno')

    matriculas_candidatos = matriculas.filter(
        status='c').select_related('aluno')

    if request.method == 'POST':
        for i in request.POST.getlist("candidatos_selecionados"):
            if i != 'csrfmiddlewaretoken':
                matricula_candidato = Matricula.objects.get(pk=i)
                matricula_candidato.status = 's'
                matricula_candidato.save()

    context = {
        'total_aulas': total_aulas,
        'turma': turma,
        'matriculas_alunos': matriculas_alunos_array,
        'matriculas_selecionados': matriculas_selecionados,
        'matriculas_candidatos': matriculas_candidatos,
        'qnt_alunos': matriculas_alunos.count(),
        'qnt_alunos_espera': matriculas_candidatos.count() + matriculas_selecionados.count(),
        'is_cheio': turma.quantidade_permitido <= matriculas_alunos.count(),
        'realocar': turma.status == 'pre' and len(Matricula.objects.filter(turma__curso=turma.curso, status='r')) > 0,

    }

    return render(request, 'app_cursos/turmas/adm_turma_visualizar.html', context)


@staff_member_required
def visualizar_turma_editar(request, id):
    
    turma = Turma.objects.get(id=id)
    form = CadastroTurmaForm(instance=turma)

    if request.method == 'POST':
        form = CadastroTurmaForm(request.POST, instance=turma)
        if form.is_valid():
            turma=form.save()
            if turma.status == 'ati':
                matriculas = Matricula.objects.filter(turma=turma)
                for matricula in matriculas:
                    if matricula.status == 's' or matricula.status == 'c':
                        matricula.status = 'r'
                        matricula.save()
            messages.success(request, 'Turma editada com sucesso!')
            return redirect('adm_turma_visualizar', id)
        
    context = {
        'turma': turma,
        'form': form
    }
    return render(request, 'app_cursos/turmas/adm_turmas_editar_turma.html', context)


@staff_member_required
def visualizar_turma_selecionado(request, matricula):
    matricula = Matricula.objects.get(pk=matricula)
    turma = Turma.objects.get(pk=matricula.turma_id)

    if turma.quantidade_permitido <= Matricula.objects.filter(turma=turma, status='a').count():
        messages.error(
            request, 'Turma cheia! Não é possível adicionar mais alunos.')
        return redirect('adm_turma_visualizar', matricula.turma.id)

    birthDate = matricula.aluno.pessoa.dt_nascimento
    today = date.today()
    age = 99
    
    if birthDate:
        age = today.year - birthDate.year - \
            ((today.month, today.day) < (birthDate.month, birthDate.day))

    form = CadastroAlunoForm(instance=matricula.aluno, prefix='aluno')
    form_responsavel = ''

    if age < 18:
        responsavel = Responsavel.objects.get(aluno=matricula.aluno)
        form_responsavel = CadastroResponsavelForm(
            instance=responsavel, prefix='responsavel')

    if request.method == 'POST':
        form_aluno = CadastroAlunoForm(
            request.POST, instance=matricula.aluno, prefix='aluno')

        if form_aluno.is_valid():

            if form_responsavel != '':
                form_responsavel = CadastroResponsavelForm(
                    instance=responsavel, prefix='responsavel')
                if form_responsavel.is_valid():
                    form_responsavel.save()
                else:
                    raise Exception('Erro no form do responsável')

            aluno = form_aluno.save()
            matricula.status = 'a'
            matricula.save()

            messages.success(request, "Candidato selecionado cadastrado como aluno!")
        return redirect('adm_turma_visualizar', matricula.turma.id)

    context = {
        'form': form,
        'form_responsavel': form_responsavel,
        'turma': turma,
        'selecionado': matricula.aluno,
        'matricula': matricula
    }
    return render(request, 'app_cursos/turmas/adm_turmas_editar_selecionado.html', context)


@staff_member_required
def excluir_turma(request, id):
    turma = Turma.objects.get(id=id)

    turma.delete()

    return redirect('adm_turmas_listar')

@staff_member_required
def matricular_aluno(request, id):
    if request.method == 'POST':
        form = MatriculaAlunoForm(request.POST)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.dt_inclusao = datetime.datetime.now()
            matricula.dt_ultima_atualizacao = datetime.datetime.now()
            matricula.save()
            messages.success(request, 'Aluno matriculado com sucesso!')
            return redirect('adm_aluno_visualizar', matricula.aluno.id)
    context={
        'form': MatriculaAlunoForm(initial={'aluno': id}),
    }
    return render(request, 'app_cursos/alunos/adm_aluno_matricular.html', context)
@staff_member_required
def adm_realocar(request, id):
    turma = Turma.objects.get(id=id)
    if request.method == "POST":
        candidatos_selecionados = request.POST.getlist('candidatos_selecionados')
        for candidato in candidatos_selecionados:
            matricula_antiga = Matricula.objects.get(matricula=candidato)
            matricula_antiga.status = 'd'
            try:
                matricula_nova = Matricula.objects.create(aluno=matricula_antiga.aluno, turma=turma, status='c')
                matricula_nova.save()
                matricula_antiga.save()
                messages.success(request, f'Aluno(s) realocados para a turma {turma} com sucesso!')
            except IntegrityError as e:
                if str(e) == 'UNIQUE constraint failed: cursos_matricula.matricula':
                    messages.warning(request, f'Alguns alunos realocados <b>já estão matriculados</b> na turma {turma}!')
                    return redirect('adm_turma_visualizar', turma.id)
        return redirect('adm_turma_visualizar', turma.id)
    matriculas = Matricula.objects.filter(turma__curso=turma.curso, status='r').order_by('aluno__pessoa__nome')
            
    context={
        'turma': turma,
        'candidatos': matriculas
    }
    return render(request, 'app_cursos/turmas/adm_turma_realocar.html', context)
# @staff_member_required
# def adm_realocar(request, id):
#     turma = get_object_or_404(Turma, pk=id)

#     outras_turmas = Turma.objects.filter(curso=turma.curso).exclude(id=turma.id)

#     if outras_turmas.count() == 0:
#         messages.error(request, f"Antes de alocar os alunos é necessário criar uma turma do curso {turma.curso}")
#         return redirect('adm_turma_visualizar', turma.id)
    
#     if request.method == "POST":
#         turma_nova = get_object_or_404(Turma, pk=request.POST['turma'])
#         candidatos_selecionados = request.POST.getlist('candidatos_selecionados')
#         for candidato in candidatos_selecionados:
#             matricula_antiga = Matricula.objects.get(matricula=candidato)
#             matricula_antiga.status = 'r'
#             matricula_antiga.save()

#             matricula_nova = Matricula.objects.create(turma=turma_nova, aluno=matricula_antiga.aluno, status='c')

#         messages.success(request, f'Alunos realocados para a turma {turma_nova} com sucesso!')
#         return redirect('adm_turma_visualizar', turma_nova.id)

#     matriculas = Matricula.objects.filter(turma=turma)
#     candidatos = matriculas.filter(Q(status='s') | Q(status='c')).order_by('status')

#     context = {
#         'turma': turma,
#         'outras_turmas': outras_turmas,
#         'candidatos': candidatos
#     }

#     return render(request, 'app_cursos/turmas/adm_turma_realocar.html', context)
@staff_member_required
def adm_alunos_listar(request):
    if request.method == 'POST':                
        alunos = Aluno.objects.filter(pessoa__nome__icontains=request.POST['pesquisa'])
        if alunos.count() == 0:
            alunos = Aluno.objects.filter(pessoa__cpf__icontains=request.POST['pesquisa'])
            if alunos.count() == 0:
                messages.warning(request, 'Nenhum aluno encontrado')
    else:
        alunos = Aluno.objects.all()
    paginator = Paginator(alunos, 35)
    context = {
        'alunos': paginator.get_page(request.GET.get('page')),
        'total_alunos': alunos.count(),
    }
    return render(request, 'app_cursos/alunos/adm_alunos_listar.html', context)


@staff_member_required
def adm_aluno_visualizar(request, id):
    aluno = Aluno.objects.get(pk=id)
    responsavel = ''

    try:
        responsavel = Responsavel.objects.get(aluno=aluno)
    except:
        pass

    context = {
        'aluno': aluno,
        'matriculas': Matricula.objects.filter(aluno=aluno),
        'responsavel': responsavel,
    }

    return render(request, 'app_cursos/alunos/adm_aluno_visualizar.html', context)


@staff_member_required
def adm_aluno_editar(request, id):
    aluno = Aluno.objects.get(pk=id)

    form = CadastroAlunoForm(instance=aluno)
    if request.method == 'POST':
        form = CadastroAlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno(a) editado(a) com sucesso!')
            return redirect('adm_aluno_visualizar', id)

    context = {
        'aluno': aluno,
        'form': form
    }

    return render(request, 'app_cursos/alunos/adm_aluno_editar.html', context)


@staff_member_required
def adm_aluno_excluir(request, id):
    aluno = Aluno.objects.get(id=id)

    aluno.delete()
    messages.success(request, 'Aluno excluido com sucesso')

    return redirect('adm_alunos_listar')


@staff_member_required
def desmatricular_aluno(request, matricula):

    matricula_obj = Matricula.objects.get(matricula=matricula)
    matricula_obj.status = 'd'
    matricula_obj.save()
    messages.success(request, 'Aluno desmatriculado com sucesso')

    return redirect('adm_aluno_visualizar', matricula_obj.aluno.id)


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@staff_member_required
def adm_aula_cadastrar(request, turma_id):

    turma = get_object_or_404(Turma, pk=turma_id)
    turno_choices = [(turno.id, turno)
                     for turno in Turno_estabelecido.objects.filter(turma=turma)]
    form = Aula_form()
    form.fields['associacao_turma_turno'].choices = turno_choices

    if request.method == 'POST':
        form = Aula_form(data=request.POST)
        form.fields['associacao_turma_turno'].choices = turno_choices

        if form.is_valid():
            aula = form.save()
            messages.success(request, 'Aula registra!')
            return redirect('adm_aulas_listar', turma.id)

    context = {'form': form, 'CADASTRAR': 'NOVO'}
    return render(request, 'app_cursos/aulas/adm_aula_cadastrar.html', context)


@staff_member_required
def adm_aulas_listar(request, turma_id):

    turma = get_object_or_404(Turma, pk=turma_id)
    aulas = Aula.objects.filter(associacao_turma_turno__turma=turma)

    context = {
        'turma': turma,
        'aulas': aulas
    }

    return render(request, 'app_cursos/aulas/adm_aulas_listar.html', context)


@staff_member_required
def adm_aula_visualizar(request, turma_id, aula_id):

    if request.method == "POST":
        acao = request.POST.get('acao') or 'p'
        for matricula in request.POST.getlist('alunos_selecionados'):
            presenca = Presenca.objects.get_or_create(
                matricula=Matricula.objects.get(matricula=matricula), aula_id=aula_id)[0]
            presenca.status = acao
            presenca.save()

    turma = get_object_or_404(Turma, pk=turma_id)
    aula = get_object_or_404(Aula, pk=aula_id)
    matriculas = Matricula.objects.filter(turma=turma)

    matriculados = []
    for matricula in matriculas:
        try:
            presenca = Presenca.objects.get(aula=aula, matricula=matricula)
        except:
            presenca = ''

        matriculados.append({'matricula': matricula, 'presenca': presenca})

    context = {
        'turma': turma,
        'matriculados': matriculados,
        'aula': aula,
    }

    return render(request, 'app_cursos/aulas/adm_aula_visualizar.html', context)


@staff_member_required
def adm_justificativa_cadastrar(request, presenca_id):

    form = Justificativa_form()
    presenca = get_object_or_404(Presenca, pk=presenca_id)

    if request.method == "POST":
        form = Justificativa_form(request.POST)
        if form.is_valid():
            justificativa = form.save()
            presenca.justificativa = justificativa
            presenca.save()

            messages.error(request, 'Justificativa registrada!')
            return redirect('adm_aula_visualizar', presenca.aula.associacao_turma_turno.turma.id, presenca.aula.id)

    context = {
        'presenca': presenca,
        'form': form
    }

    return render(request, 'app_cursos/justificativas/adm_justificativa_cadastrar.html', context)


@staff_member_required
def adm_justificativa_visualizar(request, presenca_id):

    presenca = get_object_or_404(Presenca, pk=presenca_id)

    context = {
        'presenca': presenca,
        'aluno': presenca.matricula.aluno
    }

    return render(request, 'app_cursos/justificativas/adm_justificativa_visualizar.html', context)


# @staff_member_required
# def adm_eventos_listar(request):

#     eventos = Evento.objects.filter(app_name='cursos')

#     context = {
#         'eventos': eventos
#     }

#     return render(request, 'app_eventos/eventos/adm_eventos_listar.html', context)


# @staff_member_required
# def adm_evento_cadastrar(request):
#     form = Evento_form(initial={'app_name': 'cursos'})
#     if request.method == 'POST':
#         form = Evento_form(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Novo evento cadastrado com sucesso!')
#             return redirect('adm_eventos_listar')

#     context = {
#         'form': form,
#     }

#     return render(request, 'app_eventos/eventos/adm_eventos_cadastrar.html', context)


# @staff_member_required
# def adm_evento_editar(request, id):
#     evento = Evento.objects.get(pk=id)

#     form = Evento_form(instance=evento)
#     if request.method == 'POST':
#         form = Evento_form(request.POST, request.FILES, instance=evento)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Evento editado com sucesso!')
#             return redirect('adm_eventos_listar')

#     context = {
#         'evento': evento,
#         'form': form
#     }

#     return render(request, 'app_eventos/eventos/adm_evento_editar.html', context)


@staff_member_required
def import_users_from_csv(csv_file_path):
    csv_file_path = '/home/hugo/Downloads/Inscri├з├гo para o Curso Livre e Gratuito de Finan├зas Pessoais da Secretaria de Ci├кncia, Tecnologia, Inova├з├гo e Educa├з├гo Profissionalizante e Superior.vento.csv'
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        turma = Turma.objects.get(id=3)

        for row in reader:
            try:
                telefone = re.sub(r'[^\w\s]', '', row['Telefone de contato']).strip().replace(" ", "")
                password = telefone[-8:]
                print(password)
                username = f"{row['Nome'].lower().split(' ')[0]}{telefone[-3:]}"
                email = row['E-mail']
                
                user = User.objects.create_user(username, email, password)
                pessoa = Pessoa.objects.create(
                    user=user, nome=row['Nome'], email=email, endereco=row['Endereço'])
                aluno = Aluno.objects.create(pessoa=pessoa)
                matricula = Matricula.objects.create(
                    aluno=aluno, turma=turma, status='c')
                
            except Exception as e:
                print(e)
###

# @staff_member_required
# def administrativo_bemestaranimal(request):
#     return render(request, 'adm/administracao.html')

# @staff_member_required
# def cadastrar_errante(request):
#     errante_form = Form_Errante()
#     especie_form = Form_Especie()

#     context = {
#         'errante_form': errante_form,
#         'especie_form': especie_form
#     }
#     if request.method == "POST":
#         errante_form = Form_Errante(request.POST, request.FILES)
#         especie_form = Form_Especie(request.POST)
#         if errante_form.is_valid():
#             if especie_form.is_valid():
#                 errante = errante_form.save(commit=False)
#                 v_especie = especie_form.save(commit=False)
#                 especie, verify = Especie.objects.get_or_create(nome_especie=v_especie.nome_especie)
#                 errante.especie = especie
#                 errante.save()
#                 messages.success(request, 'Animal cadastrado com sucesso!')
#                 return redirect('cadastrar_errante')
#     context = {
#         'errante_form': errante_form,
#         'especie_form': especie_form
#     }
#     return render(request, 'errante/animal-errante-cadastro.html', context)

# @staff_member_required
# def listar_errante(request):
#     errantes = Errante.objects.all()
#     context = {
#         'errantes':errantes
#     }
#     return render(request, 'errante/animal_errante.html', context)

# @staff_member_required
# def listar_tutor(request):
#     qntd = Tutor.objects.all().count()
#     tutores = Tutor.objects.annotate(num=Count('animal'))
#     context = {
#         'tutores':tutores,
#         'qntd':qntd,
#     }
#     return render(request, 'adm/listar-tutores.html', context)

# @staff_member_required
# def listar_animal_tutor(request, tutor_id):
#     animais = Animal.objects.filter(tutor_id=tutor_id)
#     tutor = Tutor.objects.get(pk=tutor_id).pessoa.nome
#     context = {
#         'animais':animais,
#         'tutor':tutor
#     }
#     return render(request, 'adm/listar-animais-tutor.html', context)


# @staff_member_required
# def cad_infos_extras(request, tutor_id, animal_id):
#     animal = Animal.objects.get(pk=animal_id)
#     try:
#         info = Informacoes_Extras.objects.get(animal=animal.id)
#         if info:
#             info_extras_form = Form_Info_Extras(instance=info)
#     except:
#         info_extras_form = Form_Info_Extras(initial={'animal':Animal.objects.get(pk=animal_id).id})
#     context = {
#         'info_extras_form':info_extras_form,
#         'animal':animal
#     }
#     if request.method == "POST":
#         if info:
#             info_extras_form = Form_Info_Extras(request.POST, instance=info)
#         else:
#             info_extras_form = Form_Info_Extras(request.POST)
#         if info_extras_form.is_valid():
#             info_extras_form.save()
#     return render(request, 'adm/info-extra-cadastrar.html', context)

# @staff_member_required
# def cad_catalogo_animal(request):
#     animal_form = Form_Animal()
#     especie_form = Form_Especie()
#     animal_catalogo_form = Form_Catalogo()
#     if request.method == "POST":
#         especie_form = Form_Especie(request.POST)
#         animal_form = Form_Animal(request.POST, request.FILES)
#         animal_catalogo_form = Form_Catalogo(request.POST)
#         if animal_form.is_valid() and especie_form.is_valid():
#             animal = animal_form.save(commit=False)
#             v_especie = especie_form.save(commit=False)
#             especie, verify = Especie.objects.get_or_create(nome_especie=v_especie.nome_especie)
#             animal.especie_id = especie.id
#             animal.save()
#             if animal_catalogo_form.is_valid():
#                 animal_adocao = animal_catalogo_form.save(commit=False)
#                 animal_adocao.animal=animal
#                 animal_adocao.save()
#                 messages.success(request, 'Animal cadastrado com sucesso!')
#                 animal_form = Form_Animal()
#                 especie_form = Form_Especie()
#                 animal_catalogo_form = Form_Catalogo()
#         else:
#             messages.error(request, 'Por favor, corrija os erros abaixo.')
#     context = {
#         'animal_catalogo_form':animal_catalogo_form,
#         'especie_form':especie_form,
#         'animal_form':animal_form

#     }
#     return render(request, 'catalogo/animal-catalogo-cadastrar.html', context)

# @staff_member_required
# def listar_entrevistas(request):
#     estrevistas = EntrevistaPrevia.objects.all()
#     context = {
#         'entrevistas':estrevistas
#     }
#     return render(request, 'adm/listar_entrevista_previa.html', context)

# @staff_member_required
# def questionario(request, id):
#     entrevista = EntrevistaPrevia.objects.get(pk=id)
#     form_entrevista = Form_EntrevistaPrevia(instance=entrevista)
#     context = {
#         'entrevista':entrevista,
#         'form_entrevista':form_entrevista
#     }
#     return render(request, 'adm/questionario.html', context)

# @staff_member_required
# def gerarToken(request):
#     #pra conseguir só os tutores que tem animal cadastrado
#     tutores = Tutor.objects.all()
#     count_s = 0
#     count_n = 0
#     for tutor in tutores:
#         if len(Animal.objects.filter(tutor=tutor))!=0:
#             try:
#                 TokenDesconto.objects.get(tutor=tutor)
#             except:
#                 token = generateToken(tutor.id)
#                 new = TokenDesconto.objects.create(token=token, tutor=tutor)
#                 new.save()
#                 count_s += 1
#         else:
#             count_n += 1
#     context = {
#         'tutor_animal':count_s,
#         'tutor_s_animal':count_n
#     }
#     return render(request, 'adm/gerar-token.html', context)

# @staff_member_required
# def censo(request):
#     animais_tutor = Animal.objects.exclude(tutor=None)
#     animais_tutor.filter(castrado=True)
#     errantes = Errante.objects.all().count()
#     adocao = Catalogo.objects.all().count()
#     tutores = Tutor.objects.all().count()
#     animal = Animal.objects.all()

#     #só de tutores
#     castrados = [
#         {'tipo': 'Castrados', 'quantidade': animais_tutor.filter(castrado=True).count()},
#         {'tipo': 'Não castrados', 'quantidade': animais_tutor.filter(castrado=False).count()}
#     ]
#     animais = [
#         {'tipo':'Animais c/ tutor', 'quantidade':animal.exclude(tutor=None).count(), 'color':'#d43f35'},
#         {'tipo':'Animais p/ adoção', 'quantidade':animal.filter(tutor=None).count(), 'color':'#4585F4'},
#         {'tipo':'Animais errantes', 'quantidade':errantes, 'color':'#099E57'}


#     ] #vacinados precisa de cadastro de informação extra por parte da adm
#     context = {
#         'castrados':castrados,
#         'errantes':errantes,
#         'adocao':adocao,
#         'tutores':tutores,
#         'animais':animais,
#         'animais_tutor':animais_tutor.count()
#     }
#     return render(request, 'adm/censo.html', context)

#quantidade de animais castrados e não castrados
# vacinados (mas não pede essa informação no usuário, só na hora de cadastrar as informações extras)
@staff_member_required
def gambiarra_cevest(request):
    users = User.objects.all()
    for user in users:
        try:
            pessoa = Pessoa.objects.get(user=user)
            if len(user.username) != 11: 
                user.username = pessoa.cpf  
                user.save()
            if not Aluno.objects.filter(pessoa=pessoa).exists():
                Aluno.objects.create(
                    pessoa=pessoa,
                    profissão='Não informado',
                    escolaridade='emc',
                    estado_civil='s',
                    aceita_mais_informacoes=True,
                    li_e_aceito_termos=True
                )
                print(f'Aluno criado para o usuario {user.username} - {pessoa.nome}')
        except Pessoa.DoesNotExist:
            print(f"Pessoa nao encontrada para o usuario {user.username}")
        except Exception as e:
            print(f"Erro ao criar Aluno para o usuario {user.username}: {e}")
    return redirect('/')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def adm_cadastro_aluno(request):
    form = Form_Alterar_Pessoa()
    if request.method == 'POST':
        try:
            pessoa=Pessoa.objects.get(cpf=request.POST['cpf'])
            # messages.error(request, 'Usuário já cadastrado')
        except:
            pessoa = None
            
        if not pessoa:
            form = Form_Alterar_Pessoa(request.POST)
            if form.is_valid():
                pessoa=form.save()
                partes=request.POST['dt_nascimento'].split('-')
                user = User.objects.create_user(username=str(validate_cpf(request.POST['cpf'])), first_name=request.POST['nome'] ,email=request.POST['email'] or None, password=partes[2] + partes[1] + partes[0])
                print(partes[2] + partes[1] + partes[0])
                pessoa.user=user
                pessoa.save()
                Aluno.objects.create(
                    pessoa=pessoa,
                    profissão='Não informado',
                    escolaridade='emc',
                    estado_civil='s',
                    aceita_mais_informacoes=True,
                    li_e_aceito_termos=True
                )
                # aluno.save()
                messages.success(request, 'Usuário e aluno cadastrado com sucesso!')
    else:
        try:
            aluno = Aluno.objects.get(pessoa=pessoa)
        except:
            aluno = None
        if not aluno:
            form = Form_Alterar_Pessoa(request.POST)
            if form.is_valid():
                Aluno.objects.create(
                            pessoa=pessoa,
                            profissão='Não informado',
                            escolaridade='emc',
                            estado_civil='s',
                            aceita_mais_informacoes=True,
                            li_e_aceito_termos=True
                        )
                messages.success(request, 'Pessoa cadastrada como aluno com sucesso!')
        else:
            messages.warning(request, 'Este aluno já está cadastrado')
        
    context = {
        'form': form
    }
    return render(request, 'adm/adm_cadastro.html', context) 