import re
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    img_1 = models.ImageField(upload_to='cursos_profissionais/img')
    img_2 = models.ImageField(upload_to='cursos_profissionais/img')
    link = models.CharField(max_length=150)
    validade = models.DateField()
    parceiro = models.CharField(max_length=100)
    user_register = models.ForeignKey(User, on_delete=models.CASCADE)
    data_register = models.DateTimeField(auto_now_add=True)
    destaque = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.nome} - {self.parceiro}'
    
class Lead(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome completo')
    email = models.EmailField()
    telefone = models.CharField(max_length=15, verbose_name='Whatsapp')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_register = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.curso}'
    
  
    def clean_nome(self):
        if len(self.nome.split()) < 2:
            raise ValidationError('O nome deve conter pelo menos dois nomes.')
        
    def clean_telefone(self):            
        telefone_formatado = re.sub(r'\D', '', self.telefone)
        if len(telefone_formatado) != 11:
            raise ValidationError('O whatsapp deve ter 11 dígitos, incluindo o DDD.')
        self.telefone = telefone_formatado

    def clean(self):
        super().clean()
        self.clean_nome()
        self.clean_telefone()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)