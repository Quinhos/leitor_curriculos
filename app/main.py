import os
from dotenv import load_dotenv

from app.pdf_reader import extrair_texto
from app.filtros import aplicar_filtros
from app.ia import analisar_curriculo
from app.relatorio import gerar_relatorio


def main():
    load_dotenv()

    print("=" * 55)
    print("AGÊNCIA DE EMPREGOS TECH - TRIAGEM DE CURRÍCULOS")
    print("=" * 55)

    pdf_path = input("Caminho do currículo PDF: ").strip()
    experiencia_minima = float(input("Experiência mínima (anos): ").replace(",", "."))
    salario_maximo = float(input("Orçamento máximo da vaga (R$): ").replace(",", "."))

    texto = extrair_texto(pdf_path)

    if not texto:
        print("Não foi possível extrair texto do PDF.")
        return

    filtros = aplicar_filtros(
        texto,
        experiencia_minima,
        salario_maximo
    )

    print("\n--- FILTROS ---")
    print(f"Experiência encontrada: {filtros['experiencia']:.1f} anos")
    print(f"Experiência mínima: {'OK' if filtros['experiencia_ok'] else 'NÃO ATENDIDA'}")

    if filtros["salario"]:
        print(f"Pretensão salarial: R$ {filtros['salario']:.2f}")
    else:
        print("Pretensão salarial: não identificada")

    print(f"Faixa salarial: {'OK' if filtros['salario_ok'] else 'NÃO ATENDIDA'}")
    print(f"Resultado: {'APROVADO' if filtros['aprovado'] else 'REPROVADO'}")

    analise = None

    if filtros["aprovado"]:
        if not os.getenv("OPENAI_API_KEY"):
            print("\nCurrículo aprovado, mas OPENAI_API_KEY não configurada.")
        else:
            modelo = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            print("\nExecutando análise generativa...")
            analise = analisar_curriculo(texto, modelo)

            print("\n--- PARECER DA IA ---")
            print(analise["texto"])
            print("\n--- TOKENS ---")
            print(f"Entrada: {analise['prompt_tokens']}")
            print(f"Saída: {analise['completion_tokens']}")
            print(f"Total: {analise['total_tokens']}")
            print(f"Custo estimado: US$ {analise['custo_estimado']:.6f}")

    relatorio = gerar_relatorio(pdf_path, filtros, analise)
    print(f"\nRelatório salvo em: {relatorio}")


if __name__ == "__main__":
    main()
