from django.contrib import admin
from .models import *

admin.site.register(OrdemDeServico)
admin.site.register(Funcionario_OS)
admin.site.register(Bairro)
admin.site.register(Logradouro)
admin.site.register(Tipo_OS)
admin.site.register(OS_ext)
admin.site.register(OS_Linha_Tempo)

# Register your models here.
