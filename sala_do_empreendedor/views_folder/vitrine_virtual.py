from django.shortcuts import render, redirect
from ..models import Empresa, Registro_no_vitrine_virtual, Produto
from ..forms import FormEmpresa, FormAlterarEmpresa, FormLogoEmpresa, FormCadastrarProduto
from django.contrib import messages
from autenticacao.models import Pessoa
from django.contrib.auth.decorators import login_required

@login_required()
def cadastrar_vitrine(request, id):
    if request.user.is_staff or request.user==Empresa.objects.get(id=id).user_register:
        if  request.method == 'POST':
            try:
                empresa=Empresa.objects.get(id=id)
            except:
                empresa=Empresa.objects.filter(empresa=empresa)
                if len(empresa)==0:
                    messages.error(request, 'Empresa não encontrada!')
                    return redirect('empreendedor:minha_empresa')
                elif len(empresa)>1:
                    messages.error(request, 'Mais de uma empresa encontrada! Relate isso ao administrador do sistema!')
                    return redirect('empreendedor:minha_empresa')
            Registro_no_vitrine_virtual.objects.create(empresa=empresa, user_register=request.user).save()
            messages.success(request, 'Vitrine criada com sucesso! Agora adicione seus produtos!')
            empresa.cadastrada_na_vitrine=True
            empresa.save()
            return redirect('empreendedor:minha_vitrine', id=id)
        return render(request, 'sala_do_empreendedor/vitrine-virtual/cadastrar_vitrine.html')    
    messages.error(request, 'Você não tem autorização para acessar a página solicitada!')
    return redirect('empreendedor:minha_empresa')
    


@login_required()
def minha_vitrine(request, id):
    empresa = Empresa.objects.get(id=id)
    if request.user.is_staff or request.user==empresa.user_register:
        rg_vitrine=Registro_no_vitrine_virtual.objects.get(empresa=empresa)
        produtos=Produto.objects.filter(rg_vitrine=rg_vitrine)
        context = {
            'titulo': 'Sala do Empreendedor - Minha Vitrine',
            'empresa': empresa,
            'rg_vitrine': rg_vitrine,
            'produtos': produtos,
            'pode_cadastrar': len(produtos)<3
        }
        return render(request, 'sala_do_empreendedor/vitrine-virtual/index.html', context)
    messages.error(request, 'Você não tem autorização para acessar a página solicitada!')
    return redirect('empreendedor:minha_empresa')

@login_required
def vitrine_excluir_produto(request, id, foto_id):
    empresa = Empresa.objects.get(id=id)
    if request.user.is_staff or request.user==empresa.user_register:
        rg_vitrine=Registro_no_vitrine_virtual.objects.get(empresa=empresa)
        produto=Produto.objects.get(id=foto_id, rg_vitrine=rg_vitrine)
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('empreendedor:minha_vitrine', id=id)
    messages.error(request, 'Você não tem autorização para acessar a página solicitada!')
    return redirect('empreendedor:minha_empresa')

@login_required
def enviar_ou_trocar_logo(request, id):
    empresa=Empresa.objects.get(id=id)  
    if request.user.is_staff or request.user==empresa.user_register:    
            rg_vitrine=Registro_no_vitrine_virtual.objects.get(empresa=empresa)
            form=FormLogoEmpresa(instance=rg_vitrine)
            if request.method == 'POST':
                form = FormLogoEmpresa(request.POST, request.FILES, instance=rg_vitrine)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Logo alterada com sucesso!')
                    return redirect('empreendedor:minha_vitrine', id=id)
            context={
                'form': form,
                'titulo': 'Sala do Empreendedor - Minha Empresa - Enviar ou Trocar Logo'            
                }
            return render(request, 'sala_do_empreendedor/vitrine-virtual/enviar_ou_trocar_logo.html', context)
    messages.error(request, 'Você não tem autorização para acessar a página solicitada!')
    return redirect('empreendedor:minha_empresa') 

@login_required()
def casdastrar_produto(request, id):
    empresa=Empresa.objects.get(id=id)  
    if request.user.is_staff or request.user==empresa.user_register:
        rg_vitrine=Registro_no_vitrine_virtual.objects.get(empresa=empresa)
        form=FormCadastrarProduto(initial={'rg_vitrine': rg_vitrine.id})
        if request.method == 'POST':
                form = FormCadastrarProduto(request.POST, request.FILES)
                if form.is_valid():
                    produto=form.save(commit=False)
                    produto.rg_vitrine=rg_vitrine
                    produto.save()
                    messages.success(request, 'Produto cadastrado com sucesso!')
                    return redirect('empreendedor:minha_vitrine', id=id)
        context={
            'form': form,
            'titulo': 'Sala do Empreendedor - Vitrine Virtual - Cadastrar produto'
            }
        return render(request, 'sala_do_empreendedor/vitrine-virtual/cadastrar_produto.html', context)
    messages.error(request, 'Você não tem autorização para acessar a página solicitada!')
    return redirect('empreendedor:minha_empresa')
    
@login_required()
def cadastrar_produto_vitrine(request):
    form=FormEmpresa()
    if request.method == 'POST':
        form = FormEmpresa(request.POST)
        if form.is_valid():
            empresa=form.save()
            empresa.user_register=request.user
            empresa.save()
            messages.success(request, 'Empresa cadastrada com sucesso!')
            pessoa=Pessoa.objects.get(user=request.user)
            pessoa.possui_cnpj=True
            pessoa.save()
            return redirect('empreendedor:minha_empresa')
    context = {
        'titulo': 'Sala do Empreendedor - Vitrine Virtual - Cadastrar empresa no Vitrine Virtual',
        'form': form
    }
    return render(request, 'sala_do_empreendedor/minha-empresa/cadastro_empresa.html', context)

@login_required()
def editar_vitrine(request, id):
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
            'titulo': 'Sala do Empreendedor - Vitrine Virtual - Editar dados da vitrine',
            'form': form
        }
        return render(request, 'sala_do_empreendedor/minha-empresa/editar_empresa.html', context)
    return redirect('empreendedor:minha_empresa')
