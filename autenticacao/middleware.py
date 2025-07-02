from .models import Pessoa
from django.utils.deprecation import MiddlewareMixin

class PessoaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        
        if request.user.is_authenticated:
            try:
                request.pessoa = Pessoa.objects.get(user=request.user)
            except Pessoa.DoesNotExist:
                request.pessoa = None
        else:
            request.pessoa = None