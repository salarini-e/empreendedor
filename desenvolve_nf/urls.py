from django.urls import path
from . import views

from django.conf.urls import handler500

handler500 = 'desenvolve_nf.views.error_500'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.admin, name='admin'),
    path('solicitar/newsletter/', views.solicitarNewsLetter, name='newsletter'),
    path('get-clima-tempo/', views.getClimaTempo, name='getClimaTempo'),
    path('carnaval/', views.carnaval, name='carnaval')
]
