from pathlib import Path
from datetime import datetime


def gerar_relatorio(
    pdf_path,
    filtros,
    analise=None
):

    Path("relatorios").mkdir(
        exist_ok=True
    )

    nome = Path(pdf_path).stem

    destino = (
        Path("relatorios")
        / f"{nome}_relatorio.txt"
    )


    linhas = [

        "=" * 60,

        "             TECH TALENT AI",

        "          RELATÓRIO DE TRIAGEM",

        "=" * 60,

        "",

        f"Currículo: {pdf_path}",

        (
            "Data da análise: "
            + datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        ),

        "",

        "=" * 60,

        "1. FILTROS DETERMINÍSTICOS",

        "=" * 60,

        "",

        (
            f"Experiência encontrada: "
            f"{filtros['experiencia']:.1f} anos"
        ),

        (
            "Experiência mínima: "
            + (
                "ATENDIDA"
                if filtros["experiencia_ok"]
                else "NÃO ATENDIDA"
            )
        ),

        "",

        (
            f"Pretensão salarial: "
            f"R$ {filtros['salario']:.2f}"
            if filtros["salario"]
            else
            "Pretensão salarial: "
            "NÃO IDENTIFICADA"
        ),

        (
            "Faixa salarial: "
            + (
                "COMPATÍVEL"
                if filtros["salario_ok"]
                else "INCOMPATÍVEL"
            )
        ),

        "",

        (
            "RESULTADO FINAL: "
            + (
                "APROVADO"
                if filtros["aprovado"]
                else "REPROVADO"
            )
        ),

        ""
    ]


    if analise:

        linhas.extend([

            "=" * 60,

            "2. ANÁLISE GENERATIVA",

            "=" * 60,

            "",

            analise["texto"],

            "",

            "=" * 60,

            "3. MONITORAMENTO DE TOKENS",

            "=" * 60,

            "",

            (
                f"Tokens de entrada: "
                f"{analise['prompt_tokens']}"
            ),

            (
                f"Tokens de saída: "
                f"{analise['completion_tokens']}"
            ),

            (
                f"Tokens totais: "
                f"{analise['total_tokens']}"
            ),

            (
                f"Custo estimado: "
                f"US$ {analise['custo_estimado']:.6f}"
            ),

            ""
        ])

    else:

        linhas.extend([

            "=" * 60,

            "2. ANÁLISE GENERATIVA",

            "=" * 60,

            "",

            "A IA não foi acionada.",

            "O candidato não passou pelos "
            "filtros determinísticos.",

            ""
        ])


    linhas.extend([

        "=" * 60,

        "FIM DO RELATÓRIO",

        "=" * 60

    ])


    destino.write_text(
        "\n".join(linhas),
        encoding="utf-8"
    )


    return destino