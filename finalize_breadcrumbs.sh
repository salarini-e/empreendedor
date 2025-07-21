#!/bin/bash

echo "Verificando páginas do quero-ser-mei que ainda precisam ser atualizadas..."

# Lista de arquivos a verificar
files=(
    "o-que-voce-precisa-saber-antes-de-se-tornar-um-mei.html"
    "quaisAsOcupacoesQuePodemSerMei.html" 
    "dicasDeSegurancaDaVigilanciaSanitaria.html"
    "documentosNecessarios.html"
)

base_path="/home/eduardo/Documentos/Github/empreendedor/sala_do_empreendedor/templates/sala_do_empreendedor/quero-ser-mei"

for file in "${files[@]}"; do
    filepath="$base_path/$file"
    if [ -f "$filepath" ]; then
        echo "Verificando $file..."
        
        # Verifica se tem breadcrumb-container (CSS antigo)
        if grep -q "breadcrumb-container" "$filepath"; then
            echo "  - $file precisa ser atualizada (tem CSS antigo de breadcrumb)"
        else
            echo "  - $file está atualizada"
        fi
        
        # Verifica se tem hero section
        if grep -q "hero-section" "$filepath"; then
            echo "  - $file tem hero section"
        else
            echo "  - $file NÃO tem hero section"
        fi
        
        echo ""
    fi
done

echo "Verificação concluída."
