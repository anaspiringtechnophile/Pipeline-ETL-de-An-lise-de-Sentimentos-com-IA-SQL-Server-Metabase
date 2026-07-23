# Pipeline ETL de Análise de Sentimentos com IA, SQL Server & Metabase

Pipeline completo de Engenharia de Dados que realiza a **extração de avaliações não estruturadas de escolas de São Carlos**, processa os dados utilizando **Modelos de Linguagem (Gemini 3.6 Flash com Pydantic)**, armazena as informações estruturadas em um banco dedicado no **SQL Server (Docker)** e disponibiliza a camada de analytics através de **Matplotlib, Streamlit e Metabase**.

---

## Arquitetura da Solução

1. **Extract (Extração):** Leitura de dados não estruturados contendo feedback de usuários em formato CSV.
2. **Transform (IA & Resiliência):**
   * Processamento e estruturação inteligente via **Gemini API (`gemini-3.6-flash`)**.
   * Extração garantida em esquema JSON estrito utilizando **Pydantic**.
   * Tratamento de exceções e controle de *Rate Limit* (HTTP 429 / Quota Exceeded) com rotina de *retry* e pausas estratégicas.
3. **Load (Armazenamento Relacional Dedicado):**
   * Verificação e criação automática do banco de dados dedicado `db_analytics_escolas` (evitando o uso indevido do banco `master`).
   * Persistência automatizada do DataFrame via **SQLAlchemy + pymssql** na tabela `fato_avaliacoes_escolas`.
   * Infraestrutura gerenciada via container **MS SQL Server 2022 no Docker**.
4. **Data Delivery & Analytics (Visualização):**
   * **Script Python (Matplotlib/Seaborn):** Geração automática de relatórios em imagem (`.png`).
   * **Streamlit:** App Web interativo com KPIs, gráficos e filtros dinâmicos por escola (`http://localhost:8501`).
   * **Metabase (Docker):** Dashboard corporativo conectado ao SQL Server via rede interna Docker (`http://localhost:3000`).

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **LLM / IA:** Google GenAI SDK (`gemini-3.6-flash`), Pydantic
* **Manipulação de Dados:** Pandas
* **Banco de Dados:** Microsoft SQL Server 2022, SQLAlchemy, pymssql
* **Containers & Infra:** Docker, Docker Networks
* **Visualização:** Matplotlib, Seaborn, Streamlit, Metabase

---

## Como Executar o Projeto

### 1. Pré-requisitos
* Python 3.10+
* Docker e Docker Compose instalados e em execução
* Chave de API da Google GenAI (`GEMINI_API_KEY`)

### 2. Configuração do Ambiente Python
```bash
# Clonar o repositório

git clone [https://github.com/SEU_USUARIO/etl_ia_escolas_saocarlos.git](https://github.com/SEU_USUARIO/etl_ia_escolas_saocarlos.git)
cd etl_ia_escolas_saocarlos
```

# Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install google-genai pandas pydantic sqlalchemy pymssql matplotlib seaborn streamlit


# 3. Configurar a Variável de Ambiente

export GEMINI_API_KEY="SUA_CHAVE_GEMINI_AQUI"

---

# 4 Subir SQL Server e Metabase no Docker

# Subir o SQL Server 2022

docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=SuaSenhaSegura123!" \
   -p 1433:1433 --name sql_server_demo -d \
   [mcr.microsoft.com/mssql/server:2022-latest](https://mcr.microsoft.com/mssql/server:2022-latest)

# Subir o Metabase

docker run -d -p 3000:3000 --name metabase metabase/metabase

# Criar rede Docker e conectar ambos os containers

docker network create rede_etl
docker network connect rede_etl sql_server_demo
docker network connect rede_etl metabase

# 5. Executar o Pipeline

## 1. Processar avaliações brutas com IA
python etl_avaliacoes.py

# 2. Criar banco dedicado 'db_analytics_escolas' e carregar no SQL Server
python carregar_sql.py

# 3. Gerar relatório estático em imagem
python gerar_graficos.py

# 4. Iniciar Dashboard Interativo no Streamlit

streamlit run app_dashboard.py

# 6. Conectando o Metabase ao SQL Server

Acesse o Metabase em http://localhost:3000.

Em Add your data, selecione SQL Server:

Host: sql_server_demo (usando a rede_etl) ou 172.17.0.1

Port: 1433

Database name: db_analytics_escolas

Username: sa

Password: SuaSenhaSegura123!