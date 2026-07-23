import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configuração da página Streamlit
st.set_page_config(
    page_title="Dashboard - Escolas de São Carlos",
    page_icon="🏫",
    layout="wide"
)

# Configuração da Conexão com o SQL Server
DB_USER = "sa"
DB_PASS = "---"  # ⚠️ Substitua pela sua senha do Docker
DB_HOST = "localhost"
DB_PORT = "1433"
DB_NAME = "master"

@st.cache_data(ttl=60)
def carregar_dados():
    connection_string = f"mssql+pymssql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)
    query = "SELECT * FROM fato_avaliacoes_escolas"
    return pd.read_sql(query, con=engine)

# Título do Dashboard
st.title("🏫 Analytics CX: Escolas de São Carlos")
st.markdown("Dashboard interativo alimentado por **LLM (Gemini 3.6)** e **SQL Server no Docker**.")

try:
    df = carregar_dados()

    # --- Barra Lateral: Filtros ---
    st.sidebar.header("🔍 Filtros")
    escolas_disponiveis = ["Todas"] + list(df["nome_escola"].unique())
    escola_selecionada = st.sidebar.selectbox("Selecione uma Escola:", escolas_disponiveis)

    # Filtrando o DataFrame
    if escola_selecionada != "Todas":
        df_filtrado = df[df["nome_escola"] == escola_selecionada]
    else:
        df_filtrado = df.copy()

    # --- KPIs (Métricas Principais) ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_avaliacoes = len(df_filtrado)
    positivas = len(df_filtrado[df_filtrado["sentimento"] == "Positivo"])
    neutras = len(df_filtrado[df_filtrado["sentimento"] == "Neutro"])
    negativas = len(df_filtrado[df_filtrado["sentimento"] == "Negativo"])

    col1.metric("Total de Avaliações", total_avaliacoes)
    col2.metric("Positivas 👍", positivas)
    col3.metric("Neutras 😐", neutras)
    col4.metric("Negativas 👎", negativas)

    st.divider()

    # --- Gráficos em Colunas ---
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("📊 Distribuição de Sentimento")
        sentimento_count = df_filtrado["sentimento"].value_counts()
        st.bar_chart(sentimento_count)

    with col_graf2:
        st.subheader("🏫 Avaliações por Escola")
        escola_count = df_filtrado["nome_escola"].value_counts()
        st.bar_chart(escola_count)

    st.divider()

    # --- Tabela Detalhada ---
    st.subheader("📋 Detalhamento das Avaliações Extraídas")
    st.dataframe(
        df_filtrado[["nome_escola", "sentimento", "elogios", "reclamacoes", "avaliacao_original"]],
        use_container_width=True
    )

except Exception as e:
    st.error(f"Erro ao carregar dados do SQL Server: {e}")
