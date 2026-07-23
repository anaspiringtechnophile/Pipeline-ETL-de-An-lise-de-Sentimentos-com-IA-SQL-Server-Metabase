import pandas as pd
from sqlalchemy import create_engine, text

# Configurações de Conexão
DB_USER = "sa"
DB_PASS = "Jihah#1991"  # ⚠️ Substitua pela sua senha do Docker
DB_HOST = "localhost"
DB_PORT = "1433"
NOVO_BANCO = "db_analytics_escolas"

# 1. Conecta primeiro ao 'master' apenas para garantir a criação do novo banco de dados

engine_master = create_engine(f"mssql+pymssql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/master")

print(f"Verificando/Criando o banco de dados '{NOVO_BANCO}'...")
with engine_master.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT")
    # Cria o banco caso ele não exista
    conn.execute(text(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{NOVO_BANCO}') CREATE DATABASE [{NOVO_BANCO}];"))

# 2. Conecta ao NOVO banco de dados exclusivo do projeto
engine_projeto = create_engine(f"mssql+pymssql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{NOVO_BANCO}")

# 3. Lê o CSV e salva a tabela no banco dedicado
df = pd.read_csv("relatorio_avaliacoes_saocarlos.csv")

df.to_sql(
    name="fato_avaliacoes_escolas",
    con=engine_projeto,
    if_exists="replace",
    index=False
)

print(f"SUCESSO! Tabela 'fato_avaliacoes_escolas' populada no banco dedicado '{NOVO_BANCO}'!")