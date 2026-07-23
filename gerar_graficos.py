import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# 1. Conexão ao SQL Server
DB_USER = "sa"
DB_PASS = "---"  # ⚠️ Substitua pela sua senha do Docker
DB_HOST = "localhost"
DB_PORT = "1433"
DB_NAME = "master"

connection_string = f"mssql+pymssql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("🔌 Lendo dados diretamente da tabela no SQL Server...")
engine = create_engine(connection_string)

# Consulta SQL lendo da tabela fato que criámos

query = "SELECT * FROM fato_avaliacoes_escolas"
df = pd.read_sql(query, con=engine)

# Configuração visual do Seaborn

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# --- Gráfico 1: Distribuição de Sentimentos (Pizza) ---

contagem_sentimento = df['sentimento'].value_counts()
cores = {'Positivo': '#2ecc71', 'Neutro': '#f1c40f', 'Negativo': '#e74c3c'}
cores_lista = [cores.get(x, '#3498db') for x in contagem_sentimento.index]

axes[0].pie(
    contagem_sentimento, 
    labels=contagem_sentimento.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=cores_lista,
    explode=[0.05] * len(contagem_sentimento)
)
axes[0].set_title("Distribuição de Sentimento das Avaliações", fontsize=12, fontweight='bold')

# --- Gráfico 2: Avaliações por Escola ---

sns.countplot(
    data=df, 
    y='nome_escola', 
    hue='sentimento', 
    palette=cores, 
    ax=axes[1]
)
axes[1].set_title("Sentimento por Escola em São Carlos", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Quantidade de Avaliações")
axes[1].set_ylabel("Escola")

plt.tight_layout()

# Salvando a imagem do dashboard

nome_imagem = "dashboard_analise_sentimento.png"
plt.savefig(nome_imagem, dpi=300)
print(f"✅ Gráfico salvo com sucesso como '{nome_imagem}'!")
