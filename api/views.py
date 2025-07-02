from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from requests import request
from rest_framework.parsers import JSONParser

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.decorators import api_view

from cursos.models import Curso, Alertar_Aluno_Sobre_Nova_Turma
from sala_do_empreendedor.models import Empresa

from .serializer import FornecedoresSerializer, AlertaAlunoSerializer, CursosSerializer

class Listar_Empresas(generics.ListAPIView):
    queryset=Empresa.objects.all()
    serializer_class=FornecedoresSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
class Listar_Cursos(generics.ListAPIView):
    queryset=Curso.objects.all()
    serializer_class=CursosSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
  
class AlunosInteressadosView(generics.ListAPIView):
    serializer_class = AlertaAlunoSerializer

    def get_queryset(self):
        # Obtenha o ID do curso da URL
        curso_id = self.kwargs['curso_id']
        
        # Obtenha os alunos interessados no curso
        queryset = Alertar_Aluno_Sobre_Nova_Turma.objects.filter(curso_id=curso_id, alertado=False)
        return queryset
