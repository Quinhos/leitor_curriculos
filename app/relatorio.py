from pathlib import Path
from datetime import datetime


def gerar_relatorio(pdf_path, filtros, analise=None):
    Path("relatorios").mkdir(exist_ok=True)

    nome = Path(pdf_path).stem
    destino = Path("relatorios") / f"{nome}_relatorio.txt"

    linhas = [
        "RELATÓRIO DE TRIAGEM - AGÊNCIA DE EMPREGOS TECH",
        "=" * 55,
        f"Currículo: {pdf_path}",
        f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "",
        "FILTROS DETERMINÍSTICOS",
        f"Experiência encontrada: {filtros['experiencia']:.1f} anos",
        f"Experiência mínima atendida: {'SIM' if filtros['experiencia_ok'] else 'NÃO'}",
        f"Pretensão salarial: R$ {filtros['salario']:.2f}" if filtros['salario'] else "Pretensão salarial: não identificada",
        f"Faixa salarial atendida: {'SIM' if filtros['salario_ok'] else 'NÃO'}",
        f"Resultado: {'APROVADO' if filtros['aprovado'] else 'REPROVADO'}",
        ""
    ]

    if analise:
        linhas += [
            "ANÁLISE GENERATIVA",
            "-" * 55,
            analise["texto"],
            "",
            "MONITORAMENTO DE TOKENS",
            f"Tokens de entrada: {analise['prompt_tokens']}",
            f"Tokens de saída: {analise['completion_tokens']}",
            f"Tokens totais: {analise['total_tokens']}",
            f"Custo estimado: US$ {analise['custo_estimado']:.6f}",
        ]
    else:
        linhas.append("A análise generativa não foi executada porque o currículo não passou nos filtros.")

    destino.write_text("\n".join(linhas), encoding="utf-8")
    return destino
