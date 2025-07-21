#!/bin/bash

echo "Limpando CSS antigo de breadcrumb das páginas restantes..."

# Lista de arquivos que precisam de limpeza
files=(
    "quaisAsOcupacoesQuePodemSerMei.html"
    "dicasDeSegurancaDaVigilanciaSanitaria.html" 
    "documentosNecessarios.html"
)

base_path="/home/eduardo/Documentos/Github/empreendedor/sala_do_empreendedor/templates/sala_do_empreendedor/quero-ser-mei"

for file in "${files[@]}"; do
    filepath="$base_path/$file"
    if [ -f "$filepath" ]; then
        echo "Processando $file..."
        
        # Remove CSS antigo de breadcrumb usando sed
        sed -i '/\.breadcrumb-container {/,/}/d' "$filepath"
        sed -i '/\.breadcrumb-custom {/,/}/d' "$filepath"
        sed -i '/\.breadcrumb-item-custom {/,/}/d' "$filepath"
        sed -i '/\.breadcrumb-current {/,/}/d' "$filepath"
        sed -i '/\.breadcrumb-separator {/,/}/d' "$filepath"
        
        # Remove linhas específicas de media query relacionadas ao breadcrumb
        sed -i '/\.breadcrumb-custom {/,/}/d' "$filepath"
        sed -i '/\.breadcrumb-container {/,/}/d' "$filepath"
        
        echo "  - Limpeza concluída para $file"
    else
        echo "  - Arquivo $file não encontrado"
    fi
done

echo "Limpeza de CSS concluída."
