from django import template
from datetime import date
import locale
from ..models import Solicitacao_de_Compras, Item_Solicitacao, Proposta_Item, Empresa
from ..functions.pdde import Menor_Valor_Proposto, Maior_Valor_Proposto
register = template.Library()

@register.filter(name='contarProcessos')
def contarProcessos(value):
    valor = Solicitacao_de_Compras.objects.filter(status__in=['0', '1' , '2'], escola=value).count()
    return valor

@register.filter(name='contarItensProcessos')
def contarItensProcessos(value):
    valor = Item_Solicitacao.objects.filter(solicitacao_de_compra__id=value).count()
    return valor

@register.filter(name='limitarCaracteres')
def limitarCaracteres(value, qnt):
    qnt_caracteres=len(value)
    if qnt_caracteres > qnt:
        valor = value[:qnt] + '...'
    else:
        valor = value
    return valor

@register.filter(name='contarPropostas')
def contarPropostas(value):
    valor = Proposta_Item.objects.filter(item_solicitacao__id=value).count()
    return valor

@register.filter(name='formatarPreco')
def formatarPreco(value):
    if value != 0:
        valor = '{:,.2f}'.format(value / 100).replace('.', '##').replace(',', '.').replace('##', ',')
    else:
        valor='0,00'
    return valor

@register.filter(name='menorValorProposta')
def menorValorProposta(value):
    valor = Menor_Valor_Proposto(value)
    return valor['menor_valor']

@register.filter(name='menorEmpresaProposta')
def menorEmpresaProposta(value):
    valor = Menor_Valor_Proposto(value)
    if valor['empresa'] == 'Nenhuma proposta realizada.':
        nome_da_empresa = valor['empresa']
    else:
        nome_da_empresa = Empresa.objects.get(id=valor['empresa']).nome
    return nome_da_empresa

@register.filter(name='maiorValorProposta')
def maiorValorProposta(value):
    valor = Maior_Valor_Proposto(value)
    return valor['maior_valor']

@register.filter(name='maiorEmpresaProposta')
def maiorEmpresaProposta(value):
    valor = Maior_Valor_Proposto(value)
    if valor['empresa'] == 'Nenhuma proposta realizada.':
        nome_da_empresa = valor['empresa']
    else:
        nome_da_empresa = Empresa.objects.get(id=valor['empresa']).nome
    return nome_da_empresa

@register.filter(name='valorUnitario')
def valorUnitario(value, qnt):
    if value != 0:
        valor = '{:,.2f}'.format(int(value.replace('.', '').replace(',', ''))/(qnt*100)).replace('.', '##').replace(',', '.').replace('##', ',')
    else:
        valor='0,00'
    return valor
