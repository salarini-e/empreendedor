import locale
import random
import hashlib
import string
from django.db import connection
from ..models import Item_Solicitacao, Empresa, Contrato_de_Servico, Proposta, Proposta_Item, Solicitacao_de_Compras
from ..forms import Criar_Item_Solicitacao
from django.db.models import Sum

def Menor_Valor_Proposto(item_id):
    item=Item_Solicitacao.objects.get(id=item_id)
    query = f"SELECT MIN(preco), proposta_id FROM sala_do_empreendedor_proposta_item WHERE item_solicitacao_id = {item.id};"
    with connection.cursor() as cursor:
        cursor.execute(query)
        dados = cursor.fetchone()
        menor_valor=dados[0]
        if menor_valor == None:
            menor_valor = 0
            empresa='Nenhuma proposta realizada.'
        else:
            print(menor_valor)
            menor_valor = '{:,.2f}'.format(menor_valor/ 100).replace('.', '##').replace(',', '.').replace('##', ',')
            empresa = Proposta.objects.get(id=dados[1]).empresa.id
            print(menor_valor)
    return {'item_id': item_id,'menor_valor': menor_valor, 'empresa': empresa}

def Maior_Valor_Proposto(item_id):
    item=Item_Solicitacao.objects.get(id=item_id)
    query = f"SELECT MAX(preco), proposta_id FROM sala_do_empreendedor_proposta_item WHERE item_solicitacao_id = {item.id};"
    with connection.cursor() as cursor:
        cursor.execute(query)
        dados = cursor.fetchone()
        maior_valor=dados[0]
        if maior_valor == None:
            maior_valor = 0
            empresa='Nenhuma proposta realizada.'
        else:
            maior_valor = '{:,.2f}'.format(maior_valor/100).replace('.', '##').replace(',', '.').replace('##', ',')
            empresa = Proposta.objects.get(id=dados[1]).empresa.id
    return {'item_id': item_id, 'maior_valor': maior_valor, 'empresa': empresa}


def Listar_Proposta(solicitacao_compra_id):
    solicitacao_compra = Solicitacao_de_Compras.objects.get(pk=solicitacao_compra_id)
    propostas = Proposta.objects.filter(solicitacao_de_compra=solicitacao_compra)
    lista_propostas = []

    for proposta in propostas:
        itens_proposta = Proposta_Item.objects.filter(proposta=proposta)
        valor_total = itens_proposta.aggregate(Sum('preco'))['preco__sum'] or 0
        if valor_total != 0:    
            lista_propostas.append({
                'proposta': proposta,
                'itens': itens_proposta,
                'valor_total': valor_total,
            })

    lista_propostas = sorted(lista_propostas, key=lambda x: x['valor_total'])
    return lista_propostas

def gerar_hash_contrato(numero_contrato):
    # Crie um objeto hash usando o algoritmo SHA-256
    sha256 = hashlib.sha256()
    # Atualize o objeto hash com o número do contrato convertido para bytes
    sha256.update(str(numero_contrato).encode('utf-8'))
    # Obtenha a representação hexadecimal da hash
    hash_contrato = sha256.hexdigest()
    return hash_contrato

import datetime
from django.db import transaction
def Criar_Contrato(solicitacao, request):
    proposta_vencedora = Listar_Proposta(solicitacao.id)[0]
    today = datetime.date.today()
    with transaction.atomic():
        # Criando a instância de Contrato_de_Servico
        contrato = Contrato_de_Servico.objects.create(
            solicitacao_referente=solicitacao,
            proposta_vencedora=proposta_vencedora['proposta'],
            titulo=f'Contrato nº {solicitacao.id}/{solicitacao.dt_solicitacao.year} de {solicitacao.get_tipo_display()} - {solicitacao.escola.nome}',
            proposito=solicitacao.descricao,
            hash=gerar_hash_contrato(solicitacao.id),
            user_register=request.user
        )

        # Adicionando itens associados à Proposta à instância de Contrato_de_Servico
        for proposta_item in proposta_vencedora['itens']:
            contrato.itens_solicitados.add(proposta_item.item_solicitacao)
            contrato.propostas_itens.add(proposta_item)

        # Marcando o contrato como aceito pela empresa
        contrato.aceito_pela_empresa = True

        # Salvando as alterações no banco de dados
        contrato.save()
        solicitacao.proposta_vencedora = contrato.proposta_vencedora.empresa
        solicitacao.save()
    return ['contrato-criado', contrato]

def Aceitar_Proposta(solicitacao, request):
    solicitacao.status='3'
    solicitacao.save()
    response =  Criar_Contrato(solicitacao, request)
    if response[0] == 'contrato-criado':
        return ['proposta-aceita', response[1]]
    else:
        return 'erro'

def PDDE_POST(request, solicitacao):
    if solicitacao.escola.ativa:
        if solicitacao.status == '0':
            solicitacao.status='1'
            qnt=Item_Solicitacao.objects.filter(solicitacao_de_compra=solicitacao).count()
            solicitacao.qnt_itens=qnt
            solicitacao.save()
            return 'salvo'
        else:
            response = Aceitar_Proposta(solicitacao, request)
            return response
    else:
        return 'escola-inativa'



def Divulgar_Vencedor(solicitacao):
    return 'envi'

def Enviar_Contrato(solicitacao):
    return 'envi'


# def passwd_reset(request):
#     if request.method == "POST":
#         password_reset_form = PasswordResetForm(request.POST)
#         if password_reset_form.is_valid():
#             data = password_reset_form.cleaned_data['email']
#             associated_users = User.objects.filter(email=data)
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Solicitação de alteração de senha do sistema Desenvolve NF"
#                     email_template_name = "adm/email_passwd_reset.txt"
#                     c = {
#                         "email": user.email,
#                         'domain': '127.0.0.1:8000',
#                         'site_name': 'Website',
#                         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                         "user": user,
#                         'token': default_token_generator.make_token(user),
#                         'protocol': 'https',
#                     }
#                     email = render_to_string(email_template_name, c)
#                     try:
#                         send_mail(subject, email, user.email, [
#                                   user.email], fail_silently=False)
#                     except BadHeaderError:
#                         return HttpResponse('Invalid header found.')
#                     return redirect("autenticacao:passwd_reset_done")
#     password_reset_form = PasswordResetForm()
#     return render(request=request, template_name="adm/passwd_reset.html", context={"password_reset_form": password_reset_form})
