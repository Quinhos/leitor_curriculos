import os
import tiktoken
from openai import OpenAI


def analisar_curriculo(texto: str, modelo: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Analise o currículo abaixo para uma agência de empregos focada em tecnologia.

Gere:
1. Um parecer qualitativo sobre a senioridade.
2. Uma análise das soft skills implícitas no currículo.
3. Um resumo executivo objetivo para o recrutador.

Não invente informações que não estejam no currículo.

CURRÍCULO:
{texto}
"""

    resposta = client.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": "Você é um analista de recrutamento especializado em tecnologia."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    encoding = tiktoken.encoding_for_model(modelo)

    prompt_tokens = len(encoding.encode(prompt))
    completion_text = resposta.choices[0].message.content or ""
    completion_tokens = len(encoding.encode(completion_text))
    total_tokens = prompt_tokens + completion_tokens

    # Valor de referência configurável para estimativa.
    preco_por_mil_tokens = 0.0015
    custo_estimado = (total_tokens / 1000) * preco_por_mil_tokens

    return {
        "texto": completion_text,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "custo_estimado": custo_estimado
    }
