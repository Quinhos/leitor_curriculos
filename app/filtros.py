import re


# ==========================================================
# CONFIGURAÇÕES DA VAGA
# ==========================================================

EXPERIENCIA_MINIMA_ANOS = 2
ORCAMENTO_MAXIMO = 5000.00


# ==========================================================
# EXPERIÊNCIA
# ==========================================================

def extrair_experiencia(texto):
    """
    Identifica o tempo de experiência profissional
    informado no currículo.
    """

    texto_lower = texto.lower()

    padroes = [
        r'(\d+(?:[.,]\d+)?)\s*\+?\s*anos?\s+de\s+experi',
        r'experi[êe]ncia\s+profissional\s*:\s*(\d+(?:[.,]\d+)?)\s*anos?',
        r'experi[êe]ncia\s+profissional\s*[-–]?\s*(\d+(?:[.,]\d+)?)\s*anos?',
    ]

    valores = []

    for padrao in padroes:

        encontrados = re.findall(
            padrao,
            texto_lower
        )

        for valor in encontrados:

            try:

                valor = valor.replace(",", ".")

                valores.append(
                    float(valor)
                )

            except ValueError:
                continue

    if not valores:
        return None

    return max(valores)


# ==========================================================
# SALÁRIO
# ==========================================================

def extrair_salario(texto):
    """
    Identifica a pretensão salarial do currículo.

    Aceita formatos como:

    Pretensão salarial: R$ 4.500,00
    Pretensão salarial R$ 4500
    Pretensão: 4500
    R$ 4.500,00
    """

    texto_lower = texto.lower()

    # Normaliza espaços e quebras de linha
    texto_normalizado = re.sub(
        r'\s+',
        ' ',
        texto_lower
    )

    # Primeiro procura especificamente próximo de
    # "pretensão salarial".
    padroes = [

        r'pretens[aã]o\s+salarial\s*:?\s*'
        r'r?\$?\s*'
        r'([\d.]+(?:,\d{2})?)',

        r'pretens[aã]o\s*:?\s*'
        r'r?\$?\s*'
        r'([\d.]+(?:,\d{2})?)',

        r'sal[aá]rio\s+pretendido\s*:?\s*'
        r'r?\$?\s*'
        r'([\d.]+(?:,\d{2})?)',

        r'pretende\s+receber\s*:?\s*'
        r'r?\$?\s*'
        r'([\d.]+(?:,\d{2})?)',
    ]

    for padrao in padroes:

        encontrado = re.search(
            padrao,
            texto_normalizado,
            re.IGNORECASE
        )

        if encontrado:

            valor = encontrado.group(1)

            try:

                # 4.500,00 -> 4500.00
                # 4500,00 -> 4500.00
                # 4500 -> 4500

                valor = valor.replace(
                    ".",
                    ""
                )

                valor = valor.replace(
                    ",",
                    "."
                )

                return float(valor)

            except ValueError:
                pass

    return None


# ==========================================================
# FILTRO PRINCIPAL
# ==========================================================

def verificar_requisitos(texto):
    """
    Aplica os filtros determinísticos antes da IA.
    """

    experiencia = extrair_experiencia(
        texto
    )

    salario = extrair_salario(
        texto
    )

    motivos = []

    # ======================================================
    # EXPERIÊNCIA
    # ======================================================

    if experiencia is None:

        motivos.append(
            "Não foi possível identificar "
            "o tempo de experiência."
        )

    elif experiencia < EXPERIENCIA_MINIMA_ANOS:

        motivos.append(
            f"Experiência insuficiente: "
            f"{experiencia:g} anos. "
            f"Mínimo exigido: "
            f"{EXPERIENCIA_MINIMA_ANOS} anos."
        )

    # ======================================================
    # SALÁRIO
    # ======================================================

    if salario is None:

        motivos.append(
            "Não foi possível identificar "
            "a pretensão salarial."
        )

    elif salario > ORCAMENTO_MAXIMO:

        motivos.append(
            f"Pretensão salarial de "
            f"R$ {salario:,.2f} acima do "
            f"orçamento de "
            f"R$ {ORCAMENTO_MAXIMO:,.2f}."
        )

    # ======================================================
    # RESULTADO
    # ======================================================

    aprovado = len(motivos) == 0

    return {
        "aprovado": aprovado,
        "experiencia": experiencia,
        "experiencia_minima": EXPERIENCIA_MINIMA_ANOS,
        "salario": salario,
        "orcamento_maximo": ORCAMENTO_MAXIMO,
        "motivos": motivos
    }