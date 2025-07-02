from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CadastroPCA
from .forms import CadastroPCAForm
from autenticacao.models import Pessoa, MembroPCA

from openpyxl import Workbook
from io import BytesIO
from django.http import HttpResponse

from django.shortcuts import render
from .models import CadastroPCA
from datetime import datetime
import csv

@login_required
def cadastrar_membros_pca(request):
    cadastros = CadastroPCA.objects.all()
    users = []
    for cadastro in cadastros:
        pessoa = Pessoa.objects.get(user=cadastro.user)
        if not MembroPCA.objects.filter(pessoa=pessoa).exists():
            MembroPCA.objects.create(pessoa=pessoa)
    
    return redirect('form:lista_cadastros_pca')

@login_required
def baixar_emails_pca(request):
    cadastros = CadastroPCA.objects.all()
    conteudo = []
    for cadastro in cadastros:
        conteudo.append(f'{cadastro.orgao_requisitante};{cadastro.user.first_name};{cadastro.email};{cadastro.celular_whatsapp}')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails_pca.csv"'

    writer = csv.writer(response)
    writer.writerow(['Órgão Requisitante', 'Nome', 'Email', 'Celular/WhatsApp'])

    for line in conteudo:
        writer.writerow(line.split(';'))

    return response

@login_required
def criar_cadastro_pca(request):
    if request.method == 'POST':
        form = CadastroPCAForm(request.POST)
        if form.is_valid():
            cadastro_pca = form.save(commit=False)
            cadastro_pca.user = request.user  # Atribui o usuário autenticado
            cadastro_pca.save()
            return redirect('forms:lista_cadastros_pca')  # Redireciona para a lista de cadastros após salvar
    else:
        form = CadastroPCAForm(initial={'user': request.user})

    return render(request, 'forms/pca/cadastro_pca.html', {'form': form})

@login_required
def editar_cadastro_pca(request, pk):
    cadastro_pca = get_object_or_404(CadastroPCA, pk=pk)
    
    if request.user != cadastro_pca.user:
        return redirect('forms:lista_cadastros_pca')  # Redireciona se o usuário não for o dono do cadastro

    if request.method == 'POST':
        form = CadastroPCAForm(request.POST, instance=cadastro_pca)
        if form.is_valid():
            form.save()
            return redirect('forms:lista_cadastros_pca')
    else:
        form = CadastroPCAForm(instance=cadastro_pca)

    return render(request, 'forms/pca/cadastro_pca.html', {'form': form})

@login_required
def lista_cadastros_pca(request):
    cadastros = CadastroPCA.objects.filter(user=request.user)
    return render(request, 'forms/pca/listagem_pca.html', {'cadastros': cadastros, 'titulo': 'Plano de Compras Anual'})

import os
import subprocess
from django.http import HttpResponse
from django.conf import settings
from settings.settings import db_name, db_user, db_host, db_port, db_passwd
from django.views import View

class BackupDatabaseView(View):
    def get(self, request):
        # Caminho para salvar o backup localmente
        backup_file_path = os.path.join(settings.MEDIA_ROOT, f'{db_name}_backup.sql')

        command = [
            'mysqldump',
            '-h', db_host,
            '-P', db_port,
            '-u', db_user,
            f'--password={db_passwd}',
            db_name
        ]

        try:
            # Executando o comando e salvando o backup no arquivo
            with open(backup_file_path, 'w') as backup_file:
                subprocess.run(command, stdout=backup_file, check=True)

            # Retornar o arquivo de backup como resposta para download
            with open(backup_file_path, 'rb') as backup_file:
                response = HttpResponse(backup_file.read(), content_type='application/sql')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(backup_file_path)}'
                return response

        except subprocess.CalledProcessError as e:
            # Lidar com erros durante o backup
            return HttpResponse(f"Erro ao criar backup: {str(e)}", status=500)

def export_cadastro_pca_to_excel(request):

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Cadastro PCA'

    headers = [
        'Órgão Requisitante', 
        'Subsecretaria/Departamento', 
        'Celular/WhatsApp', 
        'Email', 
        'Objeto da Licitação', 
        'Registro de Preço', 
        'Valor Estimado', 
        'Prazo de Execução', 
        'Programa de Trabalho', 
        'Data Prevista do Certame', 
        'Fonte do Recurso', 
        'Origem do Preço de Referência', 
        'Ata de Registro', 
        'Outro (especificar)', 
        'Data de Registro'
    ]
    
    worksheet.append(headers)

    for cadastro in CadastroPCA.objects.filter(dt_register__year=datetime.now().year):
        worksheet.append([
            cadastro.orgao_requisitante,
            cadastro.subsecretaria_departamento,
            cadastro.celular_whatsapp,
            cadastro.email,
            cadastro.objeto_licitacao,
            cadastro.registro_preco,
            cadastro.preco_estimado,
            cadastro.prazo_execucao,
            cadastro.programa_trabalho,
            cadastro.data_prevista_certame,
            cadastro.fonte_recurso,
            cadastro.origem_preco_referencia,
            cadastro.ata_registro,
            cadastro.outro,
            cadastro.dt_register.replace(tzinfo=None) if cadastro.dt_register else None,
        ])

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=cadastro_pca.xlsx'
    return response

def export_user_cadastro_pca_to_excel(request):

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Cadastro PCA'

    headers = [
        'Órgão Requisitante', 
        'Subsecretaria/Departamento', 
        'Celular/WhatsApp', 
        'Email', 
        'Objeto da Licitação', 
        'Registro de Preço', 
        'Valor Estimado', 
        'Prazo de Execução', 
        'Programa de Trabalho', 
        'Data Prevista do Certame', 
        'Fonte do Recurso', 
        'Origem do Preço de Referência', 
        'Ata de Registro', 
        'Outro (especificar)', 
        'Data de Registro'
    ]
    
    worksheet.append(headers)

    for cadastro in CadastroPCA.objects.filter(user=request.user, dt_register__year=datetime.now().year):
        worksheet.append([
            cadastro.orgao_requisitante,
            cadastro.subsecretaria_departamento,
            cadastro.celular_whatsapp,
            cadastro.email,
            cadastro.objeto_licitacao,
            cadastro.registro_preco,
            cadastro.preco_estimado,
            cadastro.prazo_execucao,
            cadastro.programa_trabalho,
            cadastro.data_prevista_certame,
            cadastro.fonte_recurso,
            cadastro.origem_preco_referencia,
            cadastro.ata_registro,
            cadastro.outro,
            cadastro.dt_register.replace(tzinfo=None) if cadastro.dt_register else None,
        ])

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=cadastro_pca.xlsx'
    return response
