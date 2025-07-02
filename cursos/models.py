import random
from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField

from autenticacao.models import Pessoa



class Local(models.Model):
    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = "locais"
        ordering = ['nome']

    nome = models.CharField(max_length=150, verbose_name='Nome do local')
    endereco = models.CharField(max_length=150, verbose_name='Endereço')
    bairro = models.CharField(max_length=80, verbose_name='Bairro')
    cep = models.CharField(max_length=9, verbose_name='CEP')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return '%s - %s, %s' % (self.nome, self.endereco, self.bairro)

class Instituicao(models.Model):
    class Meta:
        verbose_name = 'Instituição'
        verbose_name_plural = "Instituições"
        ordering = ['nome']

    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=6, unique=True)
    local = models.ForeignKey(Local, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.nome)


class Instituicao_Ensino_Superior(models.Model):
    class Meta:
        verbose_name = 'Instituição de Ensino Superior'
        verbose_name_plural = "Instituições de Ensino Superior"
        ordering = ['nome']

    nome = models.CharField(max_length=150)
    url = models.URLField()

    def __str__(self):
        return '%s' % (self.nome)
    
class Curso_Ensino_Superior(models.Model):
    class Meta:
        verbose_name = 'Curso de Ensino Superior'
        verbose_name_plural = "Cursos de Ensino Superior"
        ordering = ['nome']

    instituicao = models.ForeignKey(Instituicao_Ensino_Superior, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    img = models.ImageField(upload_to = 'cursos_livres/media/banner_cursos_ensino_superior/', null=True)
    url = models.URLField(default='#')

    def __str__(self):
        return '%s - %s' % (self.nome, self.instituicao)
    
class Categoria(models.Model):
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    nome = models.CharField(max_length=150, verbose_name='Nome da categoria')
    cor = ColorField(default='#FF0000')
    icone = models.ImageField(upload_to = 'cursos_livres/media/icone_categoria/', null=True)

    def __str__(self):
        return '%s' % (self.nome)

class Requisito(models.Model):
    def __str__(self):
        return '%s' % (self.descricao)
    
    descricao = models.CharField(max_length=128, verbose_name="Descrição")

class Curso(models.Model):
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = "Cursos"
        ordering = ['nome']

    TIPO = [
        ('C', 'Curso'),
        ('P', 'Palestra'),        
    ]
    TIPO_CARGA_HORARIA = [
        ('h', 'Hora'),
        ('m', 'Minuto'),        
    ]
    ESCOLARIDADES = [
        ('F', 'Ensino Fundamental'),
        ('M', 'Ensino Médio'),
        ('T', 'Ensino Técnico'),
        ('S', 'Ensino Superior'),
    ]

    tipo = models.CharField(max_length=1, choices=TIPO)
    banner = models.ImageField(upload_to = 'cursos_livres/media/banner/', null=True)
    banner_maior = models.ImageField(upload_to = 'cursos_livres/media/banner_maior/', blank=True, null=True, verbose_name='Banner maior (opcional)')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=3, unique=True)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    carga_horaria = models.IntegerField(verbose_name="Carga horária")
    tipo_carga_horaria = models.CharField(max_length=1, choices=TIPO_CARGA_HORARIA)
    descricao = models.TextField(default='')
    ativo = models.BooleanField(default=True)
    nivel_ensino = models.CharField(max_length=1, choices=ESCOLARIDADES)
    requisitos = models.ManyToManyField(Requisito)

    dt_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    dt_alteracao = models.DateField(auto_now=True)

    user_inclusao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='CursoUserInclusao')
    user_ultima_alteracao = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='CursoUserAlteracao', null=True, blank=True)

    def __str__(self):
        return '%s' % (self.nome)



class Instrutor(models.Model):
    class Meta:
        verbose_name = 'Instrutor'
        verbose_name_plural = "Instrutores"
        ordering = ['nome']

    nome = models.CharField(
        max_length=150, verbose_name='Nome completo do Instrutor')
    matricula=models.CharField(max_length=150, verbose_name='Mátricula PMNF', blank=True)
    celular = models.CharField(max_length=15, verbose_name='Celular')
    email = models.EmailField(verbose_name='Email', blank=True)
    endereco = models.CharField(
        max_length=150, blank=True, null=True, verbose_name='Endereço')
    bairro = models.CharField(max_length=80, blank=True, null=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    dt_inclusao = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '%s' % (self.nome)


class Turno(models.Model):

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = "Turnos"
        ordering = ['dia_semana', 'horario_inicio', 'horario_fim']

    DIAS_SEMANA_CHOICES = (
        ('1', 'Domingo'),
        ('2', 'Segunda-Feira'),
        ('3', 'Terça-Feira'),
        ('4', 'Quarta-Feira'),
        ('5', 'Quinta-Feira'),
        ('6', 'Sexta-Feira'),
        ('7', 'Sábado'),
    )

    dia_semana = models.CharField(max_length=1, choices=DIAS_SEMANA_CHOICES)

    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    def __str__(self):
        return '%s, de %s às %s' % (self.get_dia_semana_display(), self.horario_inicio.strftime("%H:%M"), self.horario_fim.strftime("%H:%M"))

# class Disponibilidade(models.Model):
#     disponibilidade = models.CharField(max_length=100, verbose_name='Disponibilidade')
    
#     class Meta:
#         verbose_name = 'Disponibilidade de turno'
#         verbose_name_plural = "Disponibilidade de turnos"
#         ordering = ['id']
        
#     def __str__(self):
#         return '%s' % (self.disponibilidade)
    
class Turma(models.Model):

    STATUS_CHOICES = (
        ('pre', 'Pré-inscrição'),
        ('agu', 'Aguardando'),
        ('ati', 'Ativa'),
        ('acc', 'Ativa e aceitando candidatos'),
        ('enc', 'Encerrada'),
    )

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = "Turmas"
        ordering = ['curso', 'local']

    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, verbose_name='Atividade')
    local = models.ForeignKey(Local, on_delete=models.CASCADE)

    instrutores = models.ManyToManyField(
        Instrutor, verbose_name='Instrutor(es)')
    quantidade_permitido = models.IntegerField(
        verbose_name='Quantidade de alunos permitidos')
    idade_minima = models.IntegerField(
        verbose_name='Idade mínima', null=True, blank=True)
    idade_maxima = models.IntegerField(
        verbose_name='Idade máxima', null=True, blank=True)

    data_inicio = models.DateField()
    data_final = models.DateField()

    # disponibilidade = models.ManyToManyField(Disponibilidade, verbose_name='Disponibilidade de turno')
    turnos = models.ManyToManyField(Turno, through='Turno_estabelecido')

    dt_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    dt_alteracao = models.DateTimeField(auto_now=True)

    user_inclusao = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='TurmaUserInclusao')
    user_ultima_alteracao = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='TurmaUserAlteracao', null=True, blank=True)

    status = models.CharField(max_length=3, default='pre',
                              choices=STATUS_CHOICES, verbose_name='Qual o status da turma?')
    grupo_whatsapp = models.URLField(
        blank=True, null=True, verbose_name='Link do grupo do Whatsapp')

    def __str__(self):
        turma_count = str(Turma.objects.filter(curso=self.curso, dt_inclusao__lt = self.dt_inclusao).count() + 1)

        return '%s %s/%s' % (self.curso.sigla, turma_count.rjust(3,'0'), self.data_inicio.year)


class Turno_estabelecido(models.Model):

    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    turno = models.ForeignKey(Turno, on_delete=models.PROTECT)

    def __str__(self):
        return '%s, de %s às %s' % (self.turno.get_dia_semana_display(), self.turno.horario_inicio.strftime("%H:%M"), self.turno.horario_fim.strftime("%H:%M"))

class Aluno(models.Model):

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = "Alunos"
        ordering=['pessoa__nome','dt_inclusao']

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Prefiro não informar')
    )

    ESCOLARIDADE_CHOICES = (
        ('efi', 'Ensino Fundamental Incompleto'),
        ('efc', 'Ensino Fundamental Completo'),
        ('emi', 'Ensino Médio Incompleto'),
        ('emc', 'Ensino Médio Completo'),
        ('ct', 'Curso Técnico'),
        ('esi', 'Ensino Superior Incompleto'),
        ('esc', 'Ensino Superior Completo'),
    )

    ESTADOCIVIL_CHOICES = (
        ('s', 'Solteiro(a)'),
        ('c', 'Casado(a)'),
        ('s', 'Separado(a)'),
        ('d', 'Divorciado(a)'),
        ('v', 'Viúvo(a)'),
    )

    pessoa=models.OneToOneField(Pessoa, on_delete=models.CASCADE, editable=False)

    profissão = models.CharField(max_length=150, verbose_name='Profissão', null=True)
    escolaridade = models.CharField(max_length=3, choices=ESCOLARIDADE_CHOICES, verbose_name='Escolaridade', null=True, blank=True)
    estado_civil = models.CharField(max_length=1, choices=ESTADOCIVIL_CHOICES, verbose_name='Estado Civil', null=True)
    # disponibilidade = models.ManyToManyField(Disponibilidade, verbose_name='Disponibilidade de turno')
    aceita_mais_informacoes = models.BooleanField(verbose_name='Declaro que aceito receber email com as informações das atividades', null=True, default=False)
    li_e_aceito_termos = models.BooleanField(verbose_name='Li e aceito os termos', null=True, default=False)
    dt_inclusao = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    def __str__(self):
        return '%s - %s' % (self.pessoa.nome, self.pessoa.cpf)


class Responsavel(models.Model):
    class Meta:
        verbose_name = 'Responsável'
        verbose_name_plural = "Responsáveis"
        ordering = ['nome']

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    ESTADOCIVIL_CHOICES = (
        ('s', 'Solteiro(a)'),
        ('c', 'Casado(a)'),
        ('s', 'Separado(a)'),
        ('d', 'Divorciado(a)'),
        ('v', 'Viúvo(a)'),
    )
    nome = models.CharField(
        max_length=150, verbose_name='Nome completo do responsável')
    celular = models.CharField(
        max_length=15, verbose_name='Celular p/ contato do responsável')
    email = models.EmailField(verbose_name='Email p/ contato do responsável')
    dt_nascimento = models.DateField(verbose_name='Data de Nascimento')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES,
                            verbose_name='Qual foi o sexo atribuído no seu nascimento?')
    cep = models.CharField(max_length=9, verbose_name='CEP')
    endereco = models.CharField(
        max_length=150, null=True, verbose_name='Endereço do responsável')
    bairro = models.CharField(
        verbose_name='Bairro', max_length=80, null=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    profissao = models.CharField(max_length=150, verbose_name='Profissão')
    estado_civil = models.CharField(
        max_length=1, choices=ESTADOCIVIL_CHOICES, verbose_name='Estado Civil')
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, blank=True, null=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '%s - %s' % (self.nome, self.cpf)

class Matricula(models.Model):
    STATUS_CHOICES = (
        ('c', 'Candidato'),
        ('s', 'Selecionado'),
        ('a', 'Aluno'),
        ('e', 'Desistente'),
        ('d', 'Desmatriculado'),
        ('f', 'Formado'),
        ('r', 'Realocar')
    )

    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = "Matrículas"
        ordering = ['-dt_inclusao']
        get_latest_by = 'dt_inclusao'

    def save(self, *args, **kwargs):

        turma_id = str(self.turma.id)
        aluno_id = str(self.aluno.id)
        instituicao = str(self.turma.curso.instituicao.sigla).upper()
        curso = str(self.turma.curso.sigla).upper()

        total_length = len(turma_id) + len(aluno_id) + \
            len(instituicao) + len(curso)

        if total_length > 16:
            raise ValueError(
                "O tamanho total de turma_id, aluno_id e instituicao deve ser menor ou igual a 16")

        self.matricula = instituicao + curso + \
            turma_id.rjust(16 - total_length + len(turma_id), "0") + aluno_id
        super().save(*args, **kwargs)

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    matricula = models.CharField(
        max_length=16, unique=True, editable=False, primary_key=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='c')
    dt_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    dt_ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.matricula)


class Justificativa(models.Model):
    STATUS_MOTIVO = (
        ('a', 'Ausência'),
        ('d', 'Desmatricula')
    )

    descricao = models.CharField(max_length=256, blank=True, null=True)
    motivo = models.CharField(max_length=1, choices=STATUS_MOTIVO)


class Aula(models.Model):

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = "Aulas"
        ordering = ['-dt_aula']
        unique_together = ('dt_aula', 'associacao_turma_turno')

    associacao_turma_turno = models.ForeignKey(
        Turma.turnos.through, on_delete=models.PROTECT)
    dt_aula = models.DateField(verbose_name="Data da aula")
    dt_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    descricao = models.CharField(max_length=256, verbose_name="Descrição")

    # IDEIA => Materiais de apoio
    def __str__(self):
        return f"Aula de {self.associacao_turma_turno.turma} em {self.data} das {self.horario_inicio} às {self.horario_fim}"


class Presenca(models.Model):
    class Meta:
        verbose_name = 'Presença'
        verbose_name_plural = "Presenças"
        ordering = ['-dt_inclusao']
        unique_together = ('aula', 'matricula')


    STATUS_CHOICES = (
        ('p', 'Presente'),
        ('a', 'Ausente'),
        ('c', 'Saiu mais cedo'),
    )

    aula = models.ForeignKey(Aula, on_delete=models.PROTECT)
    matricula = models.ForeignKey(Matricula, on_delete=models.PROTECT)
    justificativa = models.ForeignKey(Justificativa, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.matricula} - {self.get_status_display()}"

class Alertar_Aluno_Sobre_Nova_Turma(models.Model):
    aluno=models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='aluno_interessado')
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='curso_de_interesse')
    alertado=models.BooleanField(default=False)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Disciplinas(models.Model):
    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = "Disciplinas"
        ordering = ['nome']

    def __str__(self):
        return f'{self.curso} - {self.nome} - {self.n_aulas} - {self.carga_horaria}' 
        
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150, blank=False)
    n_aulas=models.CharField(max_length=5, blank=False)
    carga_horaria=models.CharField(max_length=5, blank=False)