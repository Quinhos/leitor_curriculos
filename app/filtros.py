import re

def extrair_experiencia(texto: str) -> float:
    padroes = [
        r"(\d+(?:[.,]\d+)?)\s*anos?\s+de\s+experi",
        r"(?:experi[êe]ncia).*?(\d+(?:[.,]\d+)?)\s*anos?"
    ]

    for padrao in padroes:
        resultado = re.search(padrao, texto, re.IGNORECASE)
        if resultado:
            return float(resultado.group(1).replace(",", "."))

    return 0.0


def extrair_pretensao_salarial(texto: str) -> float:
    padroes = [
        r"(?:pretens[aã]o|sal[aá]rio).*?R?\$?\s*([\d.]+(?:,\d+)?)",
        r"R\$\s*([\d.]+(?:,\d+)?)"
    ]

    for padrao in padroes:
        resultado = re.search(padrao, texto, re.IGNORECASE)
        if resultado:
            valor = resultado.group(1).replace(".", "").replace(",", ".")
            return float(valor)

    return 0.0


def aplicar_filtros(texto: str, experiencia_minima: float, salario_maximo: float):
    experiencia = extrair_experiencia(texto)
    salario = extrair_pretensao_salarial(texto)

    experiencia_ok = experiencia >= experiencia_minima
    salario_ok = salario == 0 or salario <= salario_maximo

    aprovado = experiencia_ok and salario_ok

    return {
        "aprovado": aprovado,
        "experiencia": experiencia,
        "salario": salario,
        "experiencia_ok": experiencia_ok,
        "salario_ok": salario_ok
    }
