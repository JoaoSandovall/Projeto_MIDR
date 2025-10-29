import pandas as pd
import pyodbc
from datetime import datetime

# --- 1. CONFIGURAÇÃO (AJUSTE SOMENTE ESTAS TRÊS LINHAS) ---
EXCEL_FILE = r'E:\projeto-MIDR\Colegiados.xlsx' 
ABA_COLEGIADOS = 'Colegiados'        # Nome da sua aba de Colegiados
ABA_REPRESENTANTES = 'Participantes' # Nome da sua aba de Representantes

# AJUSTE ESTA STRING DE CONEXÃO para seu servidor SQL Server!
DB_CONN_STRING = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"  # Ex: 'localhost\SQLEXPRESS'
    "Database=MIDR_COLEGIADOS;"
    "Trusted_Connection=yes;"
)

# --- 2. FUNÇÕES DE SUPORTE (CONEXÃO E CRIAÇÃO DE TABELAS) ---

def get_db_connection():
    """Tenta conectar ao SQL Server."""
    try:
        conn = pyodbc.connect(DB_CONN_STRING)
        print("Conexão com SQL Server estabelecida com sucesso.")
        return conn
    except pyodbc.Error as e:
        print("--- ERRO FATAL DE CONEXÃO ---")
        print(f"Não foi possível conectar ao SQL Server. Verifique a string de conexão e o driver pyodbc.")
        print(e)
        return None

def create_tables(cursor):
    """Cria todas as tabelas no SQL Server se elas ainda não existirem."""
    
    # Tabela 1: Colegiado
    SQL_CREATE_COLEGIADO = """
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Colegiado]') AND type in (N'U'))
    BEGIN
    CREATE TABLE Colegiado (
        colegiado_id INT IDENTITY(1,1) PRIMARY KEY,
        nome NVARCHAR(300) NOT NULL UNIQUE,
        status_vigencia NVARCHAR(50),
        objeto NVARCHAR(MAX),
        tipo_colegiado NVARCHAR(50),
        natureza NVARCHAR(50),
        temas NVARCHAR(255),
        link_normativo NVARCHAR(MAX),
        coordenacao NVARCHAR(255),
        atuacao_midr NVARCHAR(100),
        num_processo NVARCHAR(100)
    );
    END
    """

    # Tabela 2: Representante
    SQL_CREATE_REPRESENTANTE = """
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Representante]') AND type in (N'U'))
    BEGIN
    CREATE TABLE Representante (
        representante_id INT IDENTITY(1,1) PRIMARY KEY,
        nome NVARCHAR(255) NOT NULL,
        cargo NVARCHAR(255),
        secretaria NVARCHAR(255),
        sigla_secretaria NVARCHAR(50),
        ato_indicacao NVARCHAR(255),
        link_portaria NVARCHAR(MAX),
        data_indicacao DATE,
        num_processo NVARCHAR(100),
        CONSTRAINT UQ_Representante UNIQUE (nome, secretaria)
    );
    END
    """

    # Tabela 3: Composição (Vínculo)
    SQL_CREATE_COMPOSICAO = """
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Composicao]') AND type in (N'U'))
    BEGIN
    CREATE TABLE Composicao (
        composicao_id INT IDENTITY(1,1) PRIMARY KEY,
        colegiado_id INT NOT NULL,
        representante_id INT NOT NULL,
        ativo_representante NVARCHAR(50),
        tipo_representacao NVARCHAR(50),
        FOREIGN KEY (colegiado_id) REFERENCES Colegiado(colegiado_id),
        FOREIGN KEY (representante_id) REFERENCES Representante(representante_id),
        CONSTRAINT UQ_Composicao UNIQUE (colegiado_id, representante_id, tipo_representacao) 
    );
    END
    """
    try:
        cursor.execute(SQL_CREATE_COLEGIADO)
        cursor.execute(SQL_CREATE_REPRESENTANTE)
        cursor.execute(SQL_CREATE_COMPOSICAO)
        print("Tabelas criadas com sucesso (ou já existiam).")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        raise


# --- 3. FUNÇÕES DE IMPORTAÇÃO DE DADOS ---

def import_colegiados(conn):
    """Importa a lista de colegiados para a Tabela Colegiado."""
    cursor = conn.cursor()
    
    # 1. LEITURA E RENOMEAÇÃO (USANDO OS NOMES EXATOS DA SUA PLANILHA)
    try:
        df_colegiados = pd.read_excel(EXCEL_FILE, sheet_name=ABA_COLEGIADOS)
        # Renomeação: Excel Col Name -> BD Col Name
        df_colegiados = df_colegiados.rename(columns={
            'Nome Colegiado': 'nome',
            'Status (Vigência)': 'status_vigencia',
            'Objeto (finalidade)': 'objeto',
            'Principal/Subcolegiado': 'tipo_colegiado',
            'Interno/Interministerial': 'natureza',
            'Temas': 'temas',
            'Link do Normativo': 'link_normativo',
            'Coordenação': 'coordenacao',
            'Atuação do MDR no Colegiado': 'atuacao_midr',
            'Nº do Processo': 'num_processo'
        })
        # Limpeza e garantia de unicidade
        df_colegiados = df_colegiados.drop_duplicates(subset=['nome']).fillna('')
        print(f"Lendo {len(df_colegiados)} colegiados únicos da aba '{ABA_COLEGIADOS}'.")
        
    except Exception as e:
        print(f"ERRO ao ler a aba de Colegiados: {e}")
        return

    # 2. INSERÇÃO NA TABELA COLEGIADO
    sql = """
    IF NOT EXISTS (SELECT 1 FROM Colegiado WHERE nome = ?)
    BEGIN
        INSERT INTO Colegiado (nome, status_vigencia, objeto, tipo_colegiado, natureza, temas, link_normativo, coordenacao, atuacao_midr, num_processo) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    END
    """
    for index, row in df_colegiados.iterrows():
        try:
            params = (
                row['nome'], row['nome'], row['status_vigencia'], row['objeto'], row['tipo_colegiado'],
                row['natureza'], row['temas'], row['link_normativo'], row['coordenacao'],
                row['atuacao_midr'], row['num_processo']
            )
            cursor.execute(sql, params)
        except pyodbc.Error as e:
            print(f"Erro ao inserir colegiado '{row['nome']}': {e}")
            
    conn.commit()
    print("Importação da Tabela Colegiado concluída.")


def import_representantes_e_composicao(conn):
    """Importa representantes e cria os vínculos na tabela Composição."""
    cursor = conn.cursor()

    # 1. LEITURA E RENOMEAÇÃO (USANDO OS NOMES EXATOS DA SUA PLANILHA)
    try:
        df_representantes = pd.read_excel(EXCEL_FILE, sheet_name=ABA_REPRESENTANTES)
        # Renomeação: Excel Col Name -> BD Col Name
        df_representantes = df_representantes.rename(columns={
            'Nome Colegiado': 'nome_colegiado',
            'Representante': 'nome_representante',
            'Cargo Representante': 'cargo',
            'Secretaria Representante': 'secretaria',
            'Sigla Secretaria Representante': 'sigla_secretaria',
            'Ato Indicação Representante': 'ato_indicacao',
            'Link Portaria Representante': 'link_portaria',
            'Data Ato Indicação Representante': 'data_indicacao',
            'Nº do Processo': 'num_processo',
            'Ativo (representante)': 'ativo_representante',
            'Tipo Representação': 'tipo_representacao'
        }).fillna('') # Substitui valores NaN por string vazia para o SQL
        print(f"Lendo {len(df_representantes)} linhas da aba '{ABA_REPRESENTANTES}'.")

    except Exception as e:
        print(f"ERRO ao ler a aba de Representantes: {e}")
        return

    # 2. INSERÇÃO E VINCULAÇÃO (Representante e Composição)
    for index, row in df_representantes.iterrows():
        # Converte a data do Pandas para o formato DATE do SQL Server
        data_indicacao = None
        if row['data_indicacao']:
            try:
                # O Pandas às vezes lê a data como datetime.date ou datetime.datetime
                if isinstance(row['data_indicacao'], datetime):
                    data_indicacao = row['data_indicacao'].date()
                else: # Se for lida como string, tenta converter
                    data_indicacao = pd.to_datetime(row['data_indicacao']).date()
            except:
                pass # Se a conversão falhar, permanece None

        try:
            # --- PARTE 1: INSERIR/OBTER REPRESENTANTE ID ---
            # Busca pelo Nome + Secretaria (Chave Única)
            cursor.execute("SELECT representante_id FROM Representante WHERE nome = ? AND secretaria = ?", 
                           (row['nome_representante'], row['secretaria']))
            result_rep = cursor.fetchone()

            if result_rep is None:
                # 2. Se não existir, INSERE...
                sql_insert_rep = """
                INSERT INTO Representante (nome, cargo, secretaria, sigla_secretaria, ato_indicacao, link_portaria, data_indicacao, num_processo) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(sql_insert_rep, 
                               row['nome_representante'], row['cargo'], row['secretaria'], row['sigla_secretaria'], 
                               row['ato_indicacao'], row['link_portaria'], data_indicacao, row['num_processo'])
                
                # 3. ...e, APÓS A INSERÇÃO, BUSCA O ID RECÉM-GERADO
                # Esta instrução deve ser executada sozinha para funcionar com pyodbc
                cursor.execute("SELECT SCOPE_IDENTITY()")
                representante_id = int(cursor.fetchone()[0])
                
            else:
                # 4. Se já existir, usa o ID encontrado
                representante_id = result_rep[0]

            # --- PARTE 2: OBTER COLEGIADO ID ---
            cursor.execute("SELECT colegiado_id FROM Colegiado WHERE nome = ?", (row['nome_colegiado']))
            result_col = cursor.fetchone()
            
            if result_col is None:
                print(f"AVISO: Colegiado '{row['nome_colegiado']}' não encontrado na tabela mestra. Pulando vínculo.")
                continue
            
            colegiado_id = result_col[0]

            # --- PARTE 3: INSERIR COMPOSIÇÃO (O VÍNCULO) ---
            # Verifica se o vínculo (Colegiado + Representante + Tipo de Representação) já existe
            sql_insert_comp = """
            IF NOT EXISTS (SELECT 1 FROM Composicao WHERE colegiado_id = ? AND representante_id = ? AND tipo_representacao = ?)
            BEGIN
                INSERT INTO Composicao (colegiado_id, representante_id, ativo_representante, tipo_representacao) 
                VALUES (?, ?, ?, ?)
            END
            """
            cursor.execute(sql_insert_comp,
                           colegiado_id, representante_id, row['tipo_representacao'], # Parâmetros do IF NOT EXISTS
                           colegiado_id, representante_id, row['ativo_representante'], row['tipo_representacao']) # Parâmetros do INSERT
            
        except pyodbc.Error as e:
            print(f"Erro no vínculo de {row['nome_representante']} com {row['nome_colegiado']} (Linha {index}): {e}")
        except Exception as e:
            print(f"Erro inesperado na linha {index}: {e}")
            
    conn.commit()
    print("Importação das Tabelas Representante e Composição concluída.")


if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        print("Iniciando a criação de tabelas...")
        try:
            create_tables(conn.cursor())
            conn.commit()
        except:
            conn.close()
            exit()
        
        # A sequência é importante: Colegiados deve ser importado primeiro!
        import_colegiados(conn)
        import_representantes_e_composicao(conn)
        
        conn.close()
        print("\n--- Processo de importação finalizado. Dados estão no SQL Server. ---")