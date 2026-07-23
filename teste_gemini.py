import os
from google import genai
from pydantic import BaseModel, Field

# 1. Definimos o formato exato que queremos que a IA responda

class AnaliseAvaliacao(BaseModel):
    sentimento_geral: str = Field(description="Neutro, Positivo ou Negativo")
    elogios: list[str] = Field(description="Lista de tópicos elogiados")
    reclamacoes: list[str] = Field(description="Lista de tópicos reclamados")

# 2. Inicializa o cliente

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = """
Analise a seguinte avaliação sobre uma escola em São Carlos:
"A estrutura da escola perto do centro é excelente e os professores são nativos, o que ajuda muito na conversação. Porém, o atendimento da recepção na hora de renovar a rematrícula foi muito demorado e confuso."
"""

# 3. Chamada configurando a resposta em JSON via pydantic

response = client.models.generate_content(
    model='gemini-3.6-flash',
    contents=prompt,
    config={
        'response_mime_type': 'application/json',
        'response_schema': AnaliseAvaliacao,
    },
)

print("--- RESPOSTA EM JSON ESTRUTURADO ---")
print(response.text)