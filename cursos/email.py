from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import redirect
from django.http import HttpResponse
from autenticacao.models import Pessoa

def send_email_for_create_process(instance, historico):
    subject = f"{instance.n_protocolo} - Processo criado na Sala do Empreendedor pelo sistema Desenvolve NF!"
    email_template_name = "sala_do_empreendedor/email_criação_processo.txt"
    pessoa = Pessoa.objects.get(user=instance.solicitante)
    c = {
        "email": instance.solicitante.email,
        'subject': subject,
        'domain': 'desenvolve.novafriburgo.rj.gov.br',
        'site_name': 'Desenvolve NF',
        "user": pessoa,
        'protocol': 'https',
        'processo': instance,
        'historico': historico,
        'msg': historico.observacao,
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, instance.solicitante.email, [
                    instance.solicitante.email], fail_silently=False)
    except Exception as E:
        print(E)
        return 'Falha ao enviar email.'
    
def send_email_for_att_process(instance, historico):
    subject = f"{instance.n_protocolo} - Processo atualizado na Sala do Empreendedor no sistema Desenvolve NF!"
    email_template_name = "sala_do_empreendedor/email_att_processo.txt"
    pessoa = Pessoa.objects.get(user=instance.solicitante)
    c = {
        "email": instance.solicitante.email,
        'subject': subject,
        'domain': 'desenvolve.novafriburgo.rj.gov.br',
        'site_name': 'Desenvolve NF',
        "user": pessoa,
        'protocol': 'https',
        'processo': instance,
        'historico': historico,
        'msg': historico.observacao,
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, instance.solicitante.email, [
                    instance.solicitante.email], fail_silently=False)
    except BadHeaderError:
        return 'Invalid header found.'
    