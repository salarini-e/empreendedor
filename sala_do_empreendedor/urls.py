from django.urls import path
from . import views
 
app_name='empreendedor'
urlpatterns = [
    path('importar-empresas/', views.importar_empresas, name='importar_empresas'),
    path('', views.index, name='index'),
    path('cursos/', views.cursos, name='cursos'),
    
    path('consultar-protocolo', views.consultar_protocolo, name='consultar_protocolo'),
    
    path('conheca-nossa-sala', views.conheca_nossa_sala, name='conheca_nossa_sala'),
    
    path('minha-empresa', views.minha_empresa, name='minha_empresa'),
    path('minha-empresa/pca/', views.pca_list, name='pca'),
    path('minha-empresa/pca/download/', views.pca_list_excel_download, name='pca_download'),
    path('minha-empresa/cadastrar', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('minha-empresa/<id>/editar/', views.editar_empresa, name='editar_empresa'),
    path('minha-empresa/<id>/vitrine/', views.minha_vitrine, name='minha_vitrine'),
    path('minha-empresa/<id>/vitrine/alterar-logo', views.enviar_ou_trocar_logo, name='enviar_ou_trocar_logo'),
    path('minha-empresa/<id>/cadastrar-vitrine', views.cadastrar_vitrine, name='cadastrar_vitrine'),
    path('minha-empresa/<id>/cadastrar-vitrine/<foto_id>/excluir/', views.vitrine_excluir_produto, name='excluir_produto'),
    path('minha-empresa/<id>/vitrine/cadastrar-produto/', views.casdastrar_produto, name='cadastrar_produto'),
    path('faccao-legal/', views.faccao_legal, name='faccao_legal'),
    path('faccao-legal/cadastrar/', views.cadastrar_faccao_legal, name='cadastrar_faccao_legal'),
    path('faccao-legal/apagar/', views.apagar_faccao, name='apagar_faccao'),
    path('faccao-legal/exportar/', views.export_faccoes, name='exportar_faccao'),
    path('vitrine-virtual', views.vitrine_virtual, name='vitrine_virtual'),
    path('cadastro-fornecedores-e-compras-publicas', views.cadastro_fornecedores_e_compras_publicas, name='compras_publicas'),
    
    path('quero-ser-mei', views.quero_ser_mei, name='quero_ser_mei'),
    path('quero-ser-mei/por-que-ser-mei', views.por_que_ser_mei, name='por_que_ser_mei'),
    path('quero-ser-mei/o-que-voce-precisa-saber-antes-de-se-tornar-um-mei', views.o_que_precisa_saber_para_ser_mei, name='o_que_precisa_saber_para_ser_mei'),
    path('quero-ser-mei/jornada-empreendedora', views.jornada_empreendedora, name='jornada_empreendedora'),
    path('quero-ser-mei/documentosNecessarios', views.documentosNecessarios, name='documentosNecessarios'),
    path('quero-ser-mei/quaisAsOcupacoesQuePodemSerMei', views.quaisAsOcupacoesQuePodemSerMei, name='quaisAsOcupacoesQuePodemSerMei'),
    path('quero-ser-mei/dicasDeSegurancaDaVigilanciaSanitaria', views.dicasDeSegurancaDaVigilanciaSanitaria, name='dicasDeSegurancaDaVigilanciaSanitaria'),
    path('quero-ser-mei/dicasDeSegurançaDoCorpoDeBombeiros', views.dicasDeSegurançaDoCorpoDeBombeiros, name='dicasDeSegurançaDoCorpoDeBombeiros'),
    path('quero-ser-mei/dicasDeMeioAmbiente', views.dicasDeMeioAmbiente, name='dicasDeMeioAmbiente'),
    path('quero-ser-mei/prepareSe', views.prepareSe, name='prepareSe'),
    path('quero-ser-mei/transportadorAutonomoDeCargas', views.transportadorAutonomoDeCargas, name='transportadorAutonomoDeCargas'),
    path('quero-ser-mei/direitosEObrigacoes', views.direitosEObrigacoes, name='direitosEObrigacoes'),
    path('quero-ser-mei/registrocadastur', views.registrocadastur, name="registrocadastur"),
   
    path('ja-sou-mei', views.ja_sou_mei, name='ja_sou_mei'),
    path('ja-sou-mei/emissaoDeComprovante', views.emissaoDeComprovante, name="emissaoDeComprovante"),
    path('ja-sou-mei/atualizacaoCadastral', views.atualizacaoCadastral, name="atualizacaoCadastral"),
    path('ja-sou-mei/capacita', views.capacita, name="capacita"),
    path('ja-sou-mei/notaFiscal', views.notaFiscal, name="notaFiscal"),
    path('ja-sou-mei/relatorioMensal', views.relatorioMensal, name="relatorioMensal"),
    path('ja-sou-mei/pagamentoDeContribuicaoMensal', views.pagamentoDeContribuicaoMensal, name="pagamentoDeContribuicaoMensal"),
    path('ja-sou-mei/solucoesFinanceiras', views.solucoesFinanceiras, name="solucoesFinanceiras"),
    path('ja-sou-mei/certidoesEComprovantes', views.certidoesEComprovantes, name="certidoesEComprovantes"),
    path('ja-sou-mei/declaracaoAnualDeFaturamento', views.declaracaoAnualDeFaturamento, name="declaracaoAnualDeFaturamento"),
    path('ja-sou-mei/dispensaDeAlvara', views.dispensaDeAlvara, name="dispensaDeAlvara"),
    
    path('abertuda-de-empresa', views.abertura_de_empresa, name='abertura_de_empresa'),
    path('iss-autonomos', views.iss_autonomos, name='iss_autonomos'),
    path('legislacao', views.legislacao, name='legislacao'),
    
    path('admin/', views.sala_do_empreendedor_admin, name='admin'),
    path('admin/mapeamento-empresa-e-fornecedores', views.mapeamento_empresa_e_fornecedores, name='mapeamento_empresa_e_fornecedores'),
    path('faccao-legal/cadastrar/checkcnpj/', views.checkCNPJ, name='checkcnpj'),
    path('admin/cadastrar-profissao/', views.cadastrar_profissao, name='cadastrar_profissao'),
    
    #OPORTUNIDADES
    path('oportunidade-de-negocios', views.oportunidade_de_negocios, name='oportunidade'),
    path('oportunidade-de-negocios/natal-do-artesao/checkcpf/', views.checkCPFArtesao, name='natal_artesao_check_cpf'),
    path('oportunidade-de-negocios/natal-do-artesao/', views.natal_artesao, name='natal_artesao'),
    path('oportunidade-de-negocios/dados/', views.oportunidade_de_negocios_dados, name='dados_oportunidades'),
    path('novas-oportunidades/', views.novas_oportunidades, name='novas_oportunidades'),
    path('novas-oportunidades/exportar/', views.export_novas_oportunidades, name='novas_oportunidades_exportar'),
    path('novas-oportunidades/reuniao-sebrae/', views.redirecionamento_novas_oportunidades, name='reuniao_sebrae'),
    #PROCESSOS
    # Opções
    path('iss-autonomos', views.iss_autonomos, name='iss_autonomos'),
    path('consultar-processos/', views.consultar_processos, name='consultar_processos'),
    # Consulta do processo
    path('adm/processos-digitais/', views.processos_digitais_admin, name='processos_digitais_admin'),
    path('adm/processos-digitais/concluidos/', views.processos_concluidos, name='processos_concluidos'),
    path('adm/processos-digitais/licenca-sanitaria/', views.processo_sanitario, name='processo_sanitario'),
    path('adm/processos-digitais/concluidos/sanitario/', views.processos_concluidos_sanitario, name='novo_andamento_processo_sanitario_admin'),    
    path('consultar-processos/desenvolve/', views.meus_processos, name='listar_processos'),
    # Criar novo processo
    path('processos/criar-novo/', views.novo_processo, name='novo_processo'),
    path('processos-digitais/requerimento-ISSQ/', views.requerimento_ISSQN, name='requerimento_issqn'),
    path('processos/criar-novo/requerimento-iss/', views.em_construcao, name='requerimento_iss'),
    # path('processos/criar-novo/requerimento-iss/', views.requerimento_iss, name='requerimento_iss'),
    path('adm/processos/criar-novo/requerimento-iss/', views.requerimento_iss_admin, name='requerimento_iss_admin'),
    # Envio de documentos requeridos
    path('processos/criar-novo/envio-de-documentos/<n_protocolo>/', views.requerimento_documentos, name='requerimento_iss_doc'),
    path('processos/criar-novo/uniprofissional/envio-de-documentos/<n_protocolo>/', views.requerimento_ISSQN_doc, name='requerimento_issqn_doc'),
    # Coonsulta do processo
    path('adm/processos-digitais/andamento/<id>/', views.andamento_processo_admin, name='andamento_processo_admin'),    
    path('adm/processos-digitais/andamento/licenca-sanitaria/<id>/', views.andamento_processo_sanitario, name='andamento_processo_sanitario'),    
    path('adm/processos-digitais/andamento/licenca-ambiental/<id>/', views.andamento_processo_ambiental, name='andamento_processo_ambiental'),    
    path('processos-digitais/<protocolo>/', views.andamento_processo, name='andamento_processo'),
    # Dar andamento no processo
    path('adm/processos-digitais/<id>/novo-andamento/', views.novo_andamento_processo, name='novo_andamento_processo_admin'),
    path('adm/processos-digitais/<id>/novo-andamento/sanitario/', views.novo_andamento_processo_sanitario, name='novo_andamento_processo_sanitario_admin'),
    path('adm/processos-digitais/<id>/novo-andamento/ambiental/', views.novo_andamento_processo_ambiental, name='novo_andamento_processo_ambiental_admin'),
    # Atualizar documento do processo
    path('processos-digitais/<protocolo>/att-doc/<doc>', views.atualizar_documento_processo, name='atualizar_documento_processo'),
    
    
    
    path('checkCPF/', views.checkCPF, name='checkCPF'),
    path('checkProfissao/', views.checkProfissao, name='checkProfissao'),
    path('muda-status/', views.mudaStatus, name='mudaStatus'),
    path('muda-status-iss/', views.mudaStatus_ISS, name='mudaStatusISS'),
    path('muda-status-rg/', views.mudaStatusRG, name='mudaStatusRG'),
    path('muda-status-comprovante/', views.mudaStatusComprovante, name='mudaStatusComprovante'),
    path('muda-status-Ccertificado/', views.mudaStatusCertificado, name='mudaStatusCertificado'),
    path('muda-status-licenca/', views.mudaStatusLicenca, name='mudaStatusLicenca'),
    path('muda-status-licenca/<tipo>', views.mudaStatusLicencaComTipo, name='mudaStatusLicencaComTipo'),
    path('muda-status-espelho/', views.mudaStatusEspelho, name='mudaStatusEspelho'),
    
    # PDDE
    path('adm/pdde/', views.pdde_admin, name='pdde_admin'),
    path('pdde/', views.pdde_index, name='pdde_index'),
    path('pdde/escola/', views.pdde_index_escola, name='pdde_escola'),
    path('pdde/empresa/', views.pdde_index_empresa, name='pdde_empresa'),
    path('pdde/empresa/solicitacao/<hash>/', views.pdde_menu_opcoes_empresa, name='pdde_empresa_menu'),
    path('pdde/empresa/solicitacao/<hash>/contrato/', views.pdde_contratacao, name='pdde_contratacao'),
    path('pdde/empresa/solicitacao/<hash>/nota-fiscal/', views.pdde_nota_fiscal, name='pdde_nota_fiscal'),
    path('pdde/empresa/detalhe-solicitacao/19732<id>0977312#dd23445/', views.pdde_index_empresa_detalhe_solicitacao, name='pdde_empresa_detalhe_solicitacao'),
    
    path('adm/pdde/criar-escola/', views.pdde_criar_escola, name='pdde_criar_escola'),
    path('adm/pdde/editar-escola/', views.pdde_editar_escola, name='pdde_editar_escola'),
    path('pdde/escola/solicitacao/<hash>/confirmar-pagamento/', views.pdde_confirmar_pagamento, name='pdde_confirmar_pagamento'),
    path('adm/pdde/<id>/criar-solicitacao/', views.pdde_criar_solicitacao_de_compra, name='pdde_criar_solitacao_de_compra'),
    path('adm/pdde/<id>/listar-solicitacao/', views.pdde_listar_solicitacoes, name='pdde_listar_solicitacoes'),
    path('adm/pdde/solicitacao/<id>/detalhes/', views.pdde_criar_itens_solicitacao, name='pdde_criar_item_solicitacao'),
    path('adm/pdde/solicitacao/<id>/detalhes/item/<id_item>/', views.listar_proposta_para_o_item, name='pdde_listar_proposta_para_o_item'),
    path('adm/pdde/solicitacao/criar-item/adicionar/', views.pdde_criar_itens_solicitacao_fetch, name='pdde_criar_itens_solicitacao_fetch'),    
    path('adm/pdde/solicitacao/criar-item/remover/', views.pdde_remover_item_solicitacao_featch, name='pdde_remover_item_solicitacao_fetch'),    
    
    path('pdde/escola/solicitacao/<hash>/execucao/', views.pdde_aguardando_execucao, name='pdde_aguardando_execucao'),
    path('pdde/escola/solicitacao/<hash>/', views.pdde_menu_escola, name='pdde_menu_escola'),
    path('pdde/escola/solicitacao/<hash>/avaliar-servico/', views.pdde_avaliar_servico, name='pdde_avaliar_servico'),
    #url para rotinas diarias
    path('rotina/meia-noite/', views.atualizar_todo_dia, name='rotinas_admin'),
    
    # path('alimentar-oportunidades/', views.alimentar_oportunidades, name='alimentar_oportunidades'),
    path('linha-de-credito/solicitacao/', views.credito_facil, name='solicitacao_linha_de_credito'),    
    path('export-empresas-excel/', views.export_empresas_to_excel, name='export_empresas_to_excel'),
    path('adm/exportar-fornecedores/', views.export_empresas_to_excel, name='export_fornecedores_excel'),
    # path('adm/exportar-fornecedores/', views.export_fornecedores_excel, name='export_fornecedores_excel'),
    # 
    path('ver_requerimento/<protocolo>/', views.imprimir_documentos, name='imprimir_documentos'),
]
