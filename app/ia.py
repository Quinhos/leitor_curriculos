import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
modelo = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not api_key:
    raise ValueError("A variável OPENAI_API_KEY não foi encontrada no arquivo .env")

client = OpenAI(api_key=api_key)


def analisar_curriculo(texto):
    prompt = f"""
Você é um recrutador responsável por analisar currículos para uma vaga de tecnologia.

Analise o currículo abaixo e produza:

1. Resumo do candidato
2. Principais competências
3. Experiências relevantes
4. Pontos positivos
5. Pontos que precisam ser desenvolvidos
6. Adequação do candidato à área de Dados
7. Parecer final

Seja objetivo e profissional.

CURRÍCULO:

{texto}
"""

    resposta = client.responses.create(
        model=modelo,
        input=prompt
    )

    return resposta.output_text