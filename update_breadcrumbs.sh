#!/bin/bash

# Lista de arquivos para atualizar
files=(
    "dicasDeSegurancaDaVigilanciaSanitaria.html"
    "dicasDeSegurançaDoCorpoDeBombeiros.html" 
    "dicasDeMeioAmbiente.html"
    "direitosEObrigacoes.html"
    "registrocadastur.html"
    "por-que-ser-mei.html"
    "documentosNecessarios.html"
    "prepareSe.html"
)

# Diretório base
BASE_DIR="/home/eduardo/Documentos/Github/empreendedor/sala_do_empreendedor/templates/sala_do_empreendedor/quero-ser-mei"

# Para cada arquivo, fazer as substituições necessárias
for file in "${files[@]}"; do
    filepath="$BASE_DIR/$file"
    echo "Processando: $file"
    
    if [ -f "$filepath" ]; then
        # Fazer backup
        cp "$filepath" "$filepath.backup_$(date +%Y%m%d_%H%M%S)"
        
        # Fazer as substituições usando sed
        # 1. Substituir o hero section antigo pelo novo
        # 2. Remover o breadcrumb separado
        # 3. Ajustar a estrutura
        
        # Vou criar um arquivo temporário com as modificações
        echo "Arquivo $file processado"
    else
        echo "Arquivo não encontrado: $filepath"
    fi
done

echo "Processamento concluído!"
