from rest_framework import serializers
from cursos.models import Alertar_Aluno_Sobre_Nova_Turma, Curso

# Serializers define the API representation.
class CursosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'nome']

class AlertaAlunoSerializer(serializers.ModelSerializer):
    nome = serializers.ReadOnlyField(source='aluno.pessoa.nome')
    email = serializers.ReadOnlyField(source='aluno.pessoa.email')
    telefone = serializers.ReadOnlyField(source='aluno.pessoa.whatsapp')
    curso = serializers.ReadOnlyField(source='curso.nome')

    class Meta:
        model = Alertar_Aluno_Sobre_Nova_Turma
        fields = ['nome', 'email', 'telefone', 'curso', 'dt_inclusao']
