import csv
import pymysql
from settings.envvars import load_envars
from pathlib import Path

# Configurações iniciais
BASE_DIR = Path(__file__).resolve().parent
env_vars = load_envars(BASE_DIR)
caminho_csv = BASE_DIR / '..' / 'dados_recadastramento.csv'
nome_tabela_contribuintes = 'financas_recadastramento_pessoarecadastramento'
nome_tabela_inscricoes = 'financas_recadastramento_inscricao'

# Conectar ao banco de dados
def conectar_banco():
    return pymysql.connect(
        host=env_vars['db_host'],
        port=int(env_vars['db_port']),
        user=env_vars['db_user'],
        password=env_vars['db_pw'],
        database=env_vars['db_name'],
    )

# Processar uma linha do CSV
def processar_linha(row, cursor, contagem):
    cpf = row['CPF/CONTRIBUINTE'].strip()
    cnpj = row['CNPJ'].strip()  # Supondo que haja um campo para CNPJ

    if cpf:  # Verifica se o CPF está presente
        responsavel_tributario = row['RESPONSÁVEL TRIBUTÁRIO'].strip()
        nome_contribuinte = row['Nome Contribuinte'].strip()
        celular = row['CELULAR'].strip()
        cep = row['CEP'].strip()
        rua = row['RUA '].strip()
        numero = row['NÚMERO'].strip()
        complemento = row['COMPLEMENTO'].strip()
        bairro = row['BAIRRO'].strip()
        cidade = row['CIDADE'].strip()
        estado = row['ESTADO'].strip()
        email = row['E-MAIL'].strip()

        pessoa_recadastramento_id = None
        if not verificar_cpf_existente(cursor, cpf):
            pessoa_recadastramento_id = cadastrar_contribuinte(cursor, cpf, responsavel_tributario, nome_contribuinte, celular, cep, rua, numero, complemento, bairro, cidade, estado, email)        
            contagem['contribuintes_cadastrados'] += 1
        else:
            pessoa_recadastramento_id = obter_pessoa_recadastramento_id(cursor, cpf)  # Obter o ID se o CPF já existir
        
        inscricoes = row['INSCRIÇÃO'].split('/')
        # print(f"Processando CPF: {cpf}, ID: {pessoa_recadastramento_id}, Inscrições: {inscricoes}")
        num_inscricoes = cadastrar_inscricoes(cursor, pessoa_recadastramento_id, inscricoes)
        contagem['inscricoes_cadastradas'] += num_inscricoes

    return cpf, cnpj  # Retorna CPF e CNPJ para contagem

# Verificar se o CPF já existe no banco
def verificar_cpf_existente(cursor, cpf):
    sql = f"SELECT COUNT(*) FROM {nome_tabela_contribuintes} WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    return cursor.fetchone()[0] > 0

def obter_pessoa_recadastramento_id(cursor, cpf):
    sql = f"SELECT id FROM {nome_tabela_contribuintes} WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    return cursor.fetchone()[0]

# Cadastrar o contribuinte no banco
def cadastrar_contribuinte(cursor, cpf, responsavel_tributario, nome_contribuinte, celular, cep, rua, numero, complemento, bairro, cidade, estado, email):
    sql = f"""
    INSERT INTO {nome_tabela_contribuintes} (cpf, responsavel_tributario, nome_do_contribuinte, celular, cep, rua, numero, complemento, bairro, cidade, estado, email, cadastro_interno)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (cpf, responsavel_tributario, nome_contribuinte, celular, cep, rua, numero, complemento, bairro, cidade, estado, email, 1))

    # Retorna o ID do contribuinte recém-inserido
    return cursor.lastrowid

# Cadastrar as inscrições no banco com tratamento de exceção
def cadastrar_inscricoes(cursor, pessoa_recadastramento_id, inscricoes):
    contador_inscricoes = 0  # Contador local de inscrições
    for inscricao in inscricoes:
        inscricao = inscricao.strip()
        try:
            if not verificar_inscricao_existente(cursor, pessoa_recadastramento_id, inscricao):
                sql = f"INSERT INTO {nome_tabela_inscricoes} (pessoa_recadastramento_id, numero_inscricao) VALUES (%s, %s)"
                cursor.execute(sql, (pessoa_recadastramento_id, inscricao))
                contador_inscricoes += 1  # Incrementar contador local
        except pymysql.err.IntegrityError as e:
            if "Duplicate entry" in str(e):
                with open('log_inscricoes_repetidas.txt', 'a', encoding='utf-8') as log_file:
                    log_file.write(f"Inscrição repetida: {inscricao} para o contribuinte ID: {pessoa_recadastramento_id}\n")
            else:
                raise e  # Relançar se for um erro diferente de duplicidade
    return contador_inscricoes  # Retornar o número total de inscrições cadastradas


# Verificar se a inscrição já existe para o contribuinte
def verificar_inscricao_existente(cursor, pessoa_recadastramento_id, inscricao):
    sql = f"SELECT COUNT(*) FROM {nome_tabela_inscricoes} WHERE pessoa_recadastramento_id = %s AND numero_inscricao = %s"
    cursor.execute(sql, (pessoa_recadastramento_id, inscricao))
    return cursor.fetchone()[0] > 0



# Processar o arquivo CSV e gerar relatórios
def processar_csv():
    connection = conectar_banco()
    relatorio = {
        "sem_cpf_e_cnpj": 0,
        "sem_cpf_com_cnpj": 0
    }
    contagem = {
        "contribuintes_cadastrados": 0,
        "inscricoes_cadastradas": 0
    }
    try:
        with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            with connection.cursor() as cursor:
                for row in reader:
                    cpf, cnpj = processar_linha(row, cursor, contagem)

                    if not cpf and not cnpj:
                        relatorio["sem_cpf_e_cnpj"] += 1
                    elif not cpf and cnpj:
                        relatorio["sem_cpf_com_cnpj"] += 1
                
        connection.commit()
        
        gerar_relatorio(relatorio, contagem)  # Passar a contagem para a função de relatório

    finally:
        connection.close()

# Gerar um arquivo TXT com o relatório
def gerar_relatorio(relatorio, contagem):
    with open('relatorio.txt', 'w', encoding='utf-8') as f:
        f.write(f"Total sem CPF e CNPJ: {relatorio['sem_cpf_e_cnpj']}\n")
        f.write(f"Total sem CPF, mas com CNPJ: {relatorio['sem_cpf_com_cnpj']}\n")
        f.write(f"Total de contribuintes cadastrados: {contagem['contribuintes_cadastrados']}\n")
        f.write(f"Total de inscrições cadastradas: {contagem['inscricoes_cadastradas']}\n")

# Executar o processamento
if __name__ == "__main__":
    processar_csv()
