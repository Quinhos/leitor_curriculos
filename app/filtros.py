def verificar_requisitos(texto):
    """
    Verifica requisitos básicos do currículo.
    Retorna aprovado/reprovado e os motivos.
    """

    texto_lower = texto.lower()

    requisitos = {
        "python": "python" in texto_lower,
        "sql": "sql" in texto_lower,
        "dados": any(
    palavra in texto_lower
    for palavra in [
        "data science",
        "ciência de dados",
        "ciencia de dados",
        "data analyst",
        "data analytics",
        "analista de dados",
        "análise de dados",
        "analise de dados",
        "banco de dados",
        "banco de dados",
        "power bi",
        "business intelligence",
        "bi",
        "etl",
        "pandas",
        "numpy"
    ]
),
        "experiencia": any(
            palavra in texto_lower
            for palavra in [
                "experiência",
                "experiencia",
                "estágio",
                "estagio"
            ]
        )
    }

    motivos = []

    for requisito, encontrado in requisitos.items():
        if not encontrado:
            motivos.append(f"Não possui indicação de {requisito}")

    aprovado = len(motivos) == 0

    return {
        "aprovado": aprovado,
        "requisitos": requisitos,
        "motivos": motivos
    }