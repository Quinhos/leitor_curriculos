import os

from dotenv import load_dotenv
from ollama import chat


load_dotenv()

modelo = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")


def analisar_curriculo(texto):
    """
    Envia o currículo para o modelo local do Ollama
    e retorna a análise.
    """

    prompt = f"""
Você é um recrutador responsável por analisar currículos
para uma vaga de tecnologia com foco em Dados.

Analise o currículo abaixo e produza:

1. Resumo do candidato
2. Principais competências
3. Experiências relevantes
4. Pontos positivos
5. Pontos que precisam ser desenvolvidos
6. Adequação do candidato à área de Dados
7. Parecer final

Seja objetivo e profissional.
Baseie sua análise exclusivamente nas informações presentes
no currículo. Não invente experiências ou qualificações.

CURRÍCULO:

{texto}
"""

    resposta = chat(
        model=modelo,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return resposta.message.content