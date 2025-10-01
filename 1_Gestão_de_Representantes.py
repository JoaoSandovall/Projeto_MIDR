import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(layout="wide", page_title="Gestão de Colegiados")

DB_CONN_STRING = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;" 
    "Database=MIDR_COLEGIADOS;"
    "Trusted_Connection=yes;"
)

def get_db_connection():
    try:
        conn = pyodbc.connect(DB_CONN_STRING)
        return conn
    except pyodbc.Error as e:
        st.error(f"Erro de conexão com o Banco de Dados: {e}")
        return 
    
# Consulta (READ)

@st.cache_data(ttl=300)
def fetch_colegiados_data():
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    query = """
    SELECT 
            C.nome AS "Colegiado",
            C.status_vigencia AS "Status",
            COUNT(CP.representante_id) AS "Número de Representantes"
        FROM Colegiado C
        LEFT JOIN Composicao CP ON C.colegiado_id = CP.colegiado_id
        GROUP BY C.colegiado_id, C.nome, C.status_vigencia
        ORDER BY C.nome;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
st.title("Painel de Gestão de Colegiados")
st.markdown("Visão geral dos colegiados cadastrados no sistema.")

df_colegiados = fetch_colegiados_data()

if df_colegiados.empty:
    st.warning("Nenhum dado de colegiado encontrado. Verifique a conexão e se a importação de dados foi realizada.")
else:
    # --- MÉTRICAS DO CABEÇALHO ---
    total_colegiados = len(df_colegiados)
    ativos = df_colegiados[df_colegiados['Status'] == 'Ativo'].shape[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Colegiados", total_colegiados)
    col2.metric("Colegiados Ativos", ativos)
    col3.metric("Total de Vínculos", df_colegiados['Número de Representantes'].sum())
    
    st.markdown("---")

    # --- TABELA DE DADOS ---
    st.subheader("Lista de Colegiados")
    
    # Adicionando uma barra de busca simples
    search_term = st.text_input("Buscar por nome do colegiado:")
    if search_term:
        df_filtered = df_colegiados[df_colegiados['Colegiado'].str.contains(search_term, case=False, na=False)]
    else:
        df_filtered = df_colegiados
        
    # Exibe os dados em uma tabela interativa
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)