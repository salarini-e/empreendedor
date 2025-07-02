from sala_do_empreendedor.models import Empresa
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class FornecedoresSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Empresa
        fields = ['cnpj', 'nome', 'whatsapp', 'email']

# ViewSets define the view behavior.
# class FornecedoresViewSet(viewsets.ModelViewSet):
#     queryset = Empresa.objects.all()
#     serializer_class = FornecedoresSerializer

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'sala-do-empreendedor/get-empresas/', FornecedoresViewSet)
