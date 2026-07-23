import os
import json
import time
import pandas as pd
from google import genai
from pydantic import BaseModel, Field

# 1. Schema Pydantic
class AnaliseAvaliacao(BaseModel):
    sentimento_geral: str = Field(description="Neutro, Positivo ou Negativo")
    elogios: list[str] = Field(description="Lista de tópicos elogiados")
    reclamacoes: list[str] = Field(description="Lista de tópicos reclamados")

ARQUIVO_ENTRADA = "avaliacoes_brutas.csv"
ARQUIVO_SAIDA = "relatorio_avaliacoes_saocarlos.csv"

print(f"📖 Lendo arquivo '{ARQUIVO_ENTRADA}'...")
df_entrada = pd.read_csv(ARQUIVO_ENTRADA)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
resultados = []

print(f"🚀 Iniciando ETL de {len(df_entrada)} avaliações...\n")

for index, linha in df_entrada.iterrows():
    escola_id = linha["escola_id"]
    nome_escola = linha["nome_escola"]
    texto_avaliacao = linha["avaliacao"]
    
    print(f"[{index + 1}/{len(df_entrada)}] Analisando: {nome_escola} (ID: {escola_id})...")
    
    prompt = f"Analise a seguinte avaliação sobre a escola {nome_escola}: '{texto_avaliacao}'"
    
    sucesso = False
    tentativas = 0
    
    # Loop de tentativa com suporte a Rate Limit (HTTP 429)
    while not sucesso and tentativas < 3:
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': AnaliseAvaliacao,
                },
            )
            
            dados_ia = json.loads(response.text)
            
            resultados.append({
                "escola_id": escola_id,
                "nome_escola": nome_escola,
                "avaliacao_original": texto_avaliacao,
                "sentimento": dados_ia["sentimento_geral"],
                "elogios": ", ".join(dados_ia["elogios"]),
                "reclamacoes": ", ".join(dados_ia["reclamacoes"])
            })
            
            sucesso = True
            # Pausa de 4 segundos para manter o ritmo dentro do limite do Free Tier (15 RPM)
            time.sleep(4)
            
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                tentativas += 1
                print(f"⏳ Cota por minuto atingida. Aguardando 15 segundos para tentar novamente (Tentativa {tentativas}/3)...")
                time.sleep(15)
            else:
                print(f"❌ Erro irrecuperável na linha {index + 1}: {e}")
                break

# Load
df_resultado = pd.DataFrame(resultados)

print("\n--- RESUMO DAS AVALIAÇÕES PROCESSADAS ---")
print(df_resultado[["nome_escola", "sentimento", "elogios", "reclamacoes"]])

df_resultado.to_csv(ARQUIVO_SAIDA, index=False)
print(f"\n✅ ETL Concluído com Sucesso! Arquivo '{ARQUIVO_SAIDA}' gerado com todas as linhas.")