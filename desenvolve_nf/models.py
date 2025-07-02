from django.db import models
from autenticacao.models import Pessoa

# Create your models here.
class Carousel_Index(models.Model):
    
    nome = models.CharField(max_length=64, verbose_name="Nome para identificação ou para texto alternativo", blank=False, null=False)
    image = models.ImageField(upload_to='carousel_index/', verbose_name="Imagem 987x394", blank=False, null=True)
    url = models.CharField(max_length=164, verbose_name="Url, caso tenha para redirecionar", blank=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return '%s - %s' % (self.nome, self.id)


class ClimaTempo(models.Model):
    maxTemp = models.CharField(verbose_name="Temperatura máxima", max_length=3)
    minTemp = models.CharField(verbose_name="Temperatura mínima", max_length=3)
    madrugada = models.CharField(verbose_name="Clima na madrugada", max_length=50, blank=True)
    manha = models.CharField(verbose_name="Clima na manhã", max_length=50, blank=True)
    tarde = models.CharField(verbose_name="Clima na tarde", max_length=50, blank=True)
    noite = models.CharField(verbose_name="Clima na noite", max_length=50, blank=True)
    dt_inclusao = models.DateTimeField( auto_now_add=True, unique=True)

    def imgNameMaker(self, texto):
        texto.replace(",", "")
        palavras = texto.split(" ")
        if "noite" in palavras:
            imgName = "noite"
        elif "sol" in palavras:
            imgName = "sol"
        if "nuvens" in palavras or "nublada":
            imgName += "_nuvem"
        if "chuva" in palavras:
            imgName += "_chuva"
        if "trovoada" in palavras or "trovoadas" in palavras:
            imgName += "_trovoada"
        return imgName + ".png"


    class Meta:
        ordering = ['-dt_inclusao']
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios de clima"

    def getImg(self, turno):
        imgUrl = "/static/images/clima_icons/"
        if turno == "madrugada":
            imgUrl += self.imgNameMaker(self.madrugada)
        elif turno == "manha":
            imgUrl += self.imgNameMaker(self.manha)
        elif turno == "tarde":
            imgUrl += self.imgNameMaker(self.tarde)
        elif turno == "noite":
            imgUrl += self.imgNameMaker(self.noite)
        else:
            imgUrl += "error.png"
        return imgUrl
    
    def turno(self):
        TURNOS={
                'madrugada': [0,6],
                'manha':     [6,12],
                'tarde':     [12,18],
                'noite':     [18,00]
        }
        hora = int(self.dt_inclusao.strftime('%H'))-3
        for i in TURNOS:
            if hora >= TURNOS[i][0] and hora < TURNOS[i][1]:
                return i
            
    def timeBeholder(self):
        turno = self.turno()
        try:
            return self.getImg(turno)
        except:
            return self.getImg("erro")
        
class Solicitacao_de_cadastro_de_camera(models.Model):
    
    AUTORIZACAO_CHOICES=(
        ('S', 'Sim, eu autorizo a exibição das imagens das câmeras disponibilizadas para transmissão AO VIVO nas Redes sociais da Central de Operações e Monitoramento - Nova Friburgo Cidade Inteligente'),
        ('N', 'Não, eu não autorizo a exibição das imagens das câmeras disponibilizadas para transmissão AO VIVO'),
    )
    TIPO_CAMERA_CHOICES=(
        ('CFTV', 'CFTV - Circuito Fechado de Televisão'),
        ('VDM', 'Videomonitoramento'),
    )
    INFORMACOES_DE_ACESSO_CHOICES=(
        ('0', 'IP/DOMÍNIO'),
        ('1', 'Intelbras Cloud'),
        ('2', 'Meu equipamento NÃO É Intelbras'),
    )
    
    devidos_fins = models.BooleanField(default=False, verbose_name="Declaro para os devidos fins que meus equipamentos possuem as configurações mínimas descritas.")
    autorizacao_de_imagem = models.CharField(max_length=1, verbose_name="Autoriza a Central de Operações Nova Friburgo Cidade Inteligente a exibir as imagens captadas pelas câmeras disponibilizadas durante as transmissões ao vivo?", default='N', choices=AUTORIZACAO_CHOICES)
    tipo_camera = models.CharField(max_length=4, verbose_name="Tipo de câmera", default='CFTV', choices=TIPO_CAMERA_CHOICES)
    n_cameras = models.IntegerField(verbose_name="Número de câmeras", default=1)
    informacoes_de_acesso = models.CharField(max_length=1, verbose_name="Informações de acesso", default='0', choices=INFORMACOES_DE_ACESSO_CHOICES)
    nao_eh_intelbrass = models.CharField(max_length=64, verbose_name="Se não é Intelbras, qual a marca do seu equipamento?", blank=True)
    ip_ou_sn = models.CharField(max_length=64, verbose_name="IP/ Dominio ou (S/N) - Número de série pra acesso remoto", blank=False)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, null=True)
    atendido = models.BooleanField(default=False)
    dt_inclusao = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    
    
class Solicitacao_newsletter(models.Model):
    pessoa=models.ForeignKey(Pessoa, on_delete=models.CASCADE, null=True)