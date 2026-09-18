from pathlib import Path
import shutil

from pdf_reader import ler_curriculos
from filtros import verificar_requisitos
from ia import analisar_curriculo
from relatorio import gerar_relatorio


print("=" * 60)
print("AGÊNCIA DE EMPREGOS TECH")
print("Sistema de Triagem Automatizada de Currículos")
print("=" * 60)

print("\nIniciando análise dos currículos...")

curriculos = ler_curriculos(
    "curriculos"
)

print(
    f"Currículos encontrados: "
    f"{len(curriculos)}"
)

Path("aprovados").mkdir(
    exist_ok=True
)

Path("reprovados").mkdir(
    exist_ok=True
)


for curriculo in curriculos:

    resultado = verificar_requisitos(
        curriculo["texto"]
    )

    print(
        "\n" + "=" * 60
    )

    print(
        f"ARQUIVO: "
        f"{curriculo['arquivo']}"
    )

    print(
        "=" * 60
    )

    experiencia = resultado[
        "experiencia"
    ]

    salario = resultado[
        "salario"
    ]

    if experiencia is not None:

        print(
            f"Experiência identificada: "
            f"{experiencia:g} anos"
        )

    else:

        print(
            "Experiência identificada: "
            "não identificada"
        )

    if salario is not None:

        print(
            f"Pretensão salarial: "
            f"R$ {salario:,.2f}"
        )

    else:

        print(
            "Pretensão salarial: "
            "não identificada"
        )

    if resultado["aprovado"]:

        print(
            "\nSTATUS: APROVADO"
        )

        print(
            "\nEnviando currículo "
            "para análise da IA..."
        )

        try:

            resultado_ia = analisar_curriculo(
                curriculo["texto"]
            )

            print(
                "\nANÁLISE DA IA:"
            )

            print(
                resultado_ia["analise"]
            )

            print(
                "\n" + "-" * 60
            )

            print(
                "INFORMAÇÕES SOBRE TOKENS"
            )

            print(
                "-" * 60
            )

            print(
                f"Modelo: "
                f"{resultado_ia['modelo']}"
            )

            print(
                f"Tokens de entrada: "
                f"{resultado_ia['tokens_entrada']}"
            )

            print(
                f"Tokens de saída: "
                f"{resultado_ia['tokens_saida']}"
            )

            print(
                f"Tokens totais: "
                f"{resultado_ia['tokens_total']}"
            )

            print(
                f"Custo estimado: "
                f"R$ {resultado_ia['custo_estimado']:.2f}"
            )

            caminho_relatorio = gerar_relatorio(
                curriculo,
                resultado,
                resultado_ia
            )

            print(
                f"\nRelatório criado: "
                f"{caminho_relatorio}"
            )

            arquivo_origem = (
                Path("curriculos")
                / curriculo["arquivo"]
            )

            arquivo_destino = (
                Path("aprovados")
                / curriculo["arquivo"]
            )

            shutil.copy2(
                arquivo_origem,
                arquivo_destino
            )

            print(
                f"Currículo copiado para: "
                f"{arquivo_destino}"
            )

        except Exception as erro:

            print(
                "\nErro ao analisar "
                f"com a IA: {erro}"
            )

    else:

        print(
            "\nSTATUS: REPROVADO"
        )

        print(
            "\nMotivos:"
        )

        for motivo in resultado[
            "motivos"
        ]:

            print(
                f"- {motivo}"
            )

        caminho_relatorio = gerar_relatorio(
            curriculo,
            resultado
        )

        print(
            f"\nRelatório criado: "
            f"{caminho_relatorio}"
        )

        arquivo_origem = (
            Path("curriculos")
            / curriculo["arquivo"]
        )

        arquivo_destino = (
            Path("reprovados")
            / curriculo["arquivo"]
        )

        shutil.copy2(
            arquivo_origem,
            arquivo_destino
        )

        print(
            f"Currículo copiado para: "
            f"{arquivo_destino}"
        )


print(
    "\n" + "=" * 60
)

print(
    "PROCESSAMENTO FINALIZADO"
)

print(
    "=" * 60
)