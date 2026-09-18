import os

import tiktoken
from dotenv import load_dotenv
from ollama import chat


load_dotenv()

modelo = os.getenv(
    "OLLAMA_MODEL",
    "deepseek-r1:7b"
)


def contar_tokens(texto):

    encoding = tiktoken.get_encoding(
        "cl100k_base"
    )

    return len(
        encoding.encode(texto)
    )


def analisar_curriculo(texto):

    prompt = f"""
Você é um recrutador especializado em profissionais
do ecossistema de tecnologia.

Analise o currículo abaixo.

A análise deve obrigatoriamente conter as seguintes seções:

1. SENIORIDADE
Identifique a senioridade aparente do candidato
(Júnior, Pleno ou Sênior) e explique brevemente
os elementos do currículo que justificam essa avaliação.

2. SOFT SKILLS
Identifique soft skills que podem ser inferidas
a partir das experiências, projetos e atividades
descritas no currículo.

Não invente características que não possam ser
inferidas pelas informações fornecidas.

3. COMPETÊNCIAS TÉCNICAS
Liste as principais tecnologias, linguagens,
ferramentas e conhecimentos apresentados.

4. EXPERIÊNCIAS RELEVANTES
Resuma as experiências profissionais e acadêmicas
mais relevantes para uma vaga de tecnologia.

5. PONTOS POSITIVOS
Apresente os principais pontos fortes observados.

6. PONTOS A DESENVOLVER
Identifique conhecimentos ou competências que
poderiam ser desenvolvidos.

7. RESUMO EXECUTIVO
Crie um resumo curto e profissional do candidato,
escrito especificamente para ser enviado ao
recrutador da empresa contratante.

8. PARECER QUALITATIVO
Apresente uma conclusão objetiva sobre a aderência
do perfil à vaga de tecnologia.

Baseie toda a análise exclusivamente nas informações
presentes no currículo.

Não invente experiências, tecnologias, certificações,
formações ou características pessoais.

CURRÍCULO:

{texto}
"""

    # Contagem complementar utilizando tiktoken
    tokens_tiktoken_entrada = contar_tokens(
        prompt
    )

    resposta = chat(
        model=modelo,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    analise = resposta.message.content

    tokens_entrada = getattr(
        resposta,
        "prompt_eval_count",
        None
    )

    tokens_saida = getattr(
        resposta,
        "eval_count",
        None
    )

    if tokens_entrada is None:
        tokens_entrada = tokens_tiktoken_entrada

    if tokens_saida is None:
        tokens_saida = contar_tokens(
            analise
        )

    tokens_total = (
        tokens_entrada +
        tokens_saida
    )

    custo_estimado = 0.00

    return {
        "modelo": modelo,
        "analise": analise,
        "tokens_entrada": tokens_entrada,
        "tokens_saida": tokens_saida,
        "tokens_total": tokens_total,
        "tokens_tiktoken_entrada": tokens_tiktoken_entrada,
        "custo_estimado": custo_estimado
    }