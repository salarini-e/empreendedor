#!/bin/bash

# Script para implementar breadcrumbs modernos nas páginas MEI

# Páginas do Quero ser MEI
PAGES_QUERO_SER_MEI=(
    "quaisAsOcupacoesQuePodemSerMei"
    "dicasDeSegurancaDaVigilanciaSanitaria" 
    "dicasDeSegurançaDoCorpoDeBombeiros"
    "dicasDeMeioAmbiente"
    "prepareSe"
    "transportadorAutonomoDeCargas"
    "direitosEObrigacoes"
    "registrocadastur"
)

# Páginas do Já sou MEI
PAGES_JA_SOU_MEI=(
    "atualizacaoCadastral"
    "capacita"
    "notaFiscal"
    "relatorioMensal"
    "pagamentoDeContribuicaoMensal"
    "solucoesFinanceiras"
    "certidoesEComprovantes"
    "declaracaoAnualDeFaturamento"
    "dispensaDeAlvara"
)

BASE_PATH="/home/eduardo/Documentos/Github/empreendedor/sala_do_empreendedor/templates/sala_do_empreendedor"

echo "🚀 Implementando breadcrumbs nas páginas MEI..."

# Função para processar cada página
process_page() {
    local category=$1
    local page=$2
    local file_path="$BASE_PATH/$category/$page.html"
    
    if [ -f "$file_path" ]; then
        echo "📄 Processando: $category/$page.html"
        
        # Aqui você pode adicionar comandos sed ou outros para processar o arquivo
        # Por exemplo, remover breadcrumbs antigos e adicionar novos
        
    else
        echo "❌ Arquivo não encontrado: $file_path"
    fi
}

# Processar páginas do Quero ser MEI
echo "👤 Processando páginas 'Quero ser MEI'..."
for page in "${PAGES_QUERO_SER_MEI[@]}"; do
    process_page "quero-ser-mei" "$page"
done

# Processar páginas do Já sou MEI  
echo "✅ Processando páginas 'Já sou MEI'..."
for page in "${PAGES_JA_SOU_MEI[@]}"; do
    process_page "jaSouMei" "$page"
done

echo "✅ Script concluído!"
