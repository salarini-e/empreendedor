#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
sys.path.append('/home/eduardo/Documentos/Github/empreendedor')
django.setup()

from sala_do_empreendedor.models import Empresa, Registro_no_vitrine_virtual

def teste_vitrine():
    print("=== TESTE DA VITRINE VIRTUAL ===")
    
    # Total de empresas
    total_empresas = Empresa.objects.count()
    print(f"Total de empresas: {total_empresas}")
    
    # Empresas com perfil público
    empresas_publicas = Empresa.objects.filter(perfil_publico=True).count()
    print(f"Empresas com perfil público: {empresas_publicas}")
    
    # Total de registros na vitrine
    total_vitrine = Registro_no_vitrine_virtual.objects.count()
    print(f"Total de registros na vitrine: {total_vitrine}")
    
    # Registros na vitrine (sem filtro de perfil público)
    registros_vitrine = Registro_no_vitrine_virtual.objects.all()
    print(f"Registros que apareceriam na vitrine: {registros_vitrine.count()}")
    
    print("\n--- Empresas na vitrine ---")
    for registro in registros_vitrine:
        print(f"{registro.empresa.nome} - Perfil público: {registro.empresa.perfil_publico}")
    
    print("\n=== RESUMO ===")
    print(f"A vitrine virtual agora mostra {registros_vitrine.count()} empresas")
    print("O campo perfil_publico só afeta o acesso direto ao perfil da empresa")

if __name__ == "__main__":
    teste_vitrine()
