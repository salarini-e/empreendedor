from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('autenticacao.urls')),
    path('', include('desenvolve_nf.urls')),
    path('api/', include('api.urls')),
    path('ciencia-e-tecnologia/', include('cursos.urls')),    
    path('chat/', include('chat.urls')),
    path('sala-do-empreendedor/', include('sala_do_empreendedor.urls')),
    path('sala-do-empreendedor/', include('cursos_empresariais.urls')),
    path('sala-do-empreendedor/', include('cursos_profissionais.urls')),
    # path('senha-facil/', include('senhas_facil.urls')),
    path('administracao/', include('administracao.urls')),    
    path('django/', admin.site.urls),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
