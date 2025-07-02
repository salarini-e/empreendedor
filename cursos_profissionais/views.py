from django.shortcuts import render, redirect
from .models import Curso
from .forms import LeadForm
from django.apps import apps
from django.contrib import messages
import asyncio
from datetime import date

def index(request):
    cursos_sem_destaque = Curso.objects.filter(validade__gte=date.today(), destaque=False)
    cursos_destaque = Curso.objects.filter(validade__gte=date.today(), destaque=True)
    cursos = list(cursos_destaque) + list(cursos_sem_destaque)
    context = {
        'titulo': apps.get_app_config('cursos_profissionais').verbose_name,
        'cursos': cursos
    }
    return render(request, 'cursos_profissionais/index.html', context)


def inscrever(request, id):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            
            # loop = asyncio.new_event_loop()
            # asyncio.set_event_loop(loop)
            # loop.run_until_complete(fazer_requisicao_post(url, data))
            return redirect(Curso.objects.get(id=id).link)
    else:
        form = LeadForm(initial={'curso': id})
    context = {
        'titulo': apps.get_app_config('cursos_profissionais').verbose_name,
        'curso': Curso.objects.get(id=id),
        'form': form
    }
    return render(request, 'cursos_profissionais/inscricao.html', context)

