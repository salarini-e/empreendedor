#!/usr/bin/env python
"""
Script para ativar o perfil público de empresas para teste
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/eduardo/Documentos/Github/empreendedor')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from sala_do_empreendedor.models import Empresa, Registro_no_vitrine_virtual

def ativar_perfil_publico():
    """Ativa o perfil público de todas as empresas para teste"""
    
    print("=== ATIVANDO PERFIL PÚBLICO DAS EMPRESAS ===")
    print()
    
    # Buscar todas as empresas
    empresas = Empresa.objects.all()
    
    if not empresas.exists():
        print("❌ Nenhuma empresa encontrada no sistema!")
        return
    
    print(f"📊 Total de empresas encontradas: {empresas.count()}")
    print()
    
    # Ativar perfil público para todas as empresas
    empresas_ativadas = 0
    for empresa in empresas:
        if not empresa.perfil_publico:
            empresa.perfil_publico = True
            empresa.save()
            empresas_ativadas += 1
            print(f"✅ Empresa '{empresa.nome}' - Perfil público ATIVADO")
        else:
            print(f"ℹ️  Empresa '{empresa.nome}' - Perfil público já estava ativo")
    
    print()
    print(f"🎉 Total de empresas com perfil ativado: {empresas_ativadas}")
    
    # Verificar vitrine
    registros_vitrine = Registro_no_vitrine_virtual.objects.all()
    registros_publicos = registros_vitrine.filter(empresa__perfil_publico=True)
    
    print()
    print("=== VERIFICAÇÃO DA VITRINE ===")
    print(f"📊 Total de registros na vitrine: {registros_vitrine.count()}")
    print(f"✅ Registros na vitrine com perfil público: {registros_publicos.count()}")
    
    if registros_publicos.exists():
        print()
        print("🎯 Empresas que aparecerão na vitrine pública:")
        for registro in registros_publicos:
            print(f"   • {registro.empresa.nome}")
    
    print()
    print("✅ Processo concluído! Agora as empresas aparecerão na vitrine virtual.")
    print("🌐 Acesse a vitrine virtual para verificar: /sala-do-empreendedor/vitrine-virtual/")

def verificar_status():
    """Verifica o status atual das empresas"""
    
    print("=== STATUS ATUAL DAS EMPRESAS ===")
    print()
    
    empresas = Empresa.objects.all()
    vitrine_registros = Registro_no_vitrine_virtual.objects.all()
    
    print(f"Total de empresas: {empresas.count()}")
    print(f"Empresas com perfil público: {empresas.filter(perfil_publico=True).count()}")
    print(f"Total de registros na vitrine: {vitrine_registros.count()}")
    print(f"Registros na vitrine com perfil público: {vitrine_registros.filter(empresa__perfil_publico=True).count()}")
    print()
    
    if empresas.exists():
        print("--- Detalhes das empresas ---")
        for empresa in empresas:
            na_vitrine = vitrine_registros.filter(empresa=empresa).exists()
            print(f"• {empresa.nome} - Perfil público: {empresa.perfil_publico} - Na vitrine: {na_vitrine}")

if __name__ == "__main__":
    print("🚀 Script para gerenciar perfil público das empresas")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--verificar':
        verificar_status()
    else:
        verificar_status()
        print()
        resposta = input("Deseja ativar o perfil público de todas as empresas? (s/N): ")
        
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            print()
            ativar_perfil_publico()
        else:
            print("❌ Operação cancelada.")
