from pathlib import Path
from datetime import datetime


def gerar_relatorio(
    curriculo,
    resultado_filtro,
    resultado_ia=None
):
 
    pasta_relatorios = Path("relatorios")

    pasta_relatorios.mkdir(
        exist_ok=True
    )

    nome_arquivo = Path(
        curriculo["arquivo"]
    ).stem

    caminho_relatorio = (
        pasta_relatorios /
        f"{nome_arquivo}_relatorio.txt"
    )

    with open(
        caminho_relatorio,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            "=" * 70 + "\n"
        )

        arquivo.write(
            "RELATÓRIO DE TRIAGEM DE CURRÍCULO\n"
        )

        arquivo.write(
            "=" * 70 + "\n\n"
        )

        arquivo.write(
            f"Arquivo: {curriculo['arquivo']}\n"
        )

        arquivo.write(
            "Data da análise: "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        )

        arquivo.write(
            "\n" + "-" * 70 + "\n"
        )

        arquivo.write(
            "TRIAGEM DETERMINÍSTICA\n"
        )

        arquivo.write(
            "-" * 70 + "\n\n"
        )

        experiencia = resultado_filtro[
            "experiencia"
        ]

        experiencia_minima = resultado_filtro[
            "experiencia_minima"
        ]

        if experiencia is None:

            arquivo.write(
                "Experiência identificada: "
                "Não identificada\n"
            )

        else:

            arquivo.write(
                f"Experiência identificada: "
                f"{experiencia:g} anos\n"
            )

        arquivo.write(
            f"Experiência mínima exigida: "
            f"{experiencia_minima} anos\n"
        )

        salario = resultado_filtro[
            "salario"
        ]

        orcamento = resultado_filtro[
            "orcamento_maximo"
        ]

        if salario is None:

            arquivo.write(
                "Pretensão salarial: "
                "Não identificada\n"
            )

        else:

            arquivo.write(
                f"Pretensão salarial: "
                f"R$ {salario:,.2f}\n"
            )

        arquivo.write(
            f"Orçamento máximo da vaga: "
            f"R$ {orcamento:,.2f}\n"
        )

        arquivo.write("\n")

        if resultado_filtro["aprovado"]:

            arquivo.write(
                "STATUS: APROVADO\n"
            )

        else:

            arquivo.write(
                "STATUS: REPROVADO\n"
            )

            arquivo.write(
                "\nMotivos:\n"
            )

            for motivo in resultado_filtro[
                "motivos"
            ]:

                arquivo.write(
                    f"- {motivo}\n"
                )

        if resultado_ia:

            arquivo.write(
                "\n" + "-" * 70 + "\n"
            )

            arquivo.write(
                "ANÁLISE GENERATIVA\n"
            )

            arquivo.write(
                "-" * 70 + "\n\n"
            )

            arquivo.write(
                resultado_ia["analise"]
            )

            arquivo.write(
                "\n\n" + "-" * 70 + "\n"
            )

            arquivo.write(
                "MONITORAMENTO DE TOKENS E RECURSOS\n"
            )

            arquivo.write(
                "-" * 70 + "\n\n"
            )

            arquivo.write(
                f"Modelo: "
                f"{resultado_ia['modelo']}\n"
            )

            arquivo.write(
                f"Tokens de entrada: "
                f"{resultado_ia['tokens_entrada']}\n"
            )

            arquivo.write(
                f"Tokens de saída: "
                f"{resultado_ia['tokens_saida']}\n"
            )

            arquivo.write(
                f"Tokens totais: "
                f"{resultado_ia['tokens_total']}\n"
            )

            arquivo.write(
                f"Contagem complementar "
                f"(tiktoken): "
                f"{resultado_ia['tokens_tiktoken_entrada']}\n"
            )

            arquivo.write(
                f"Custo estimado da triagem: "
                f"R$ {resultado_ia['custo_estimado']:.2f}\n"
            )

            arquivo.write(
                "\nObservação: o modelo é executado "
                "localmente através do Ollama, portanto "
                "não há cobrança de API por token.\n"
            )

    return caminho_relatorio