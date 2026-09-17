from pdf_reader import ler_curriculos
from filtros import verificar_requisitos
from ia import analisar_curriculo


print("Iniciando análise dos currículos...")

curriculos = ler_curriculos("curriculos")

print(f"Currículos encontrados: {len(curriculos)}")


for curriculo in curriculos:

    resultado = verificar_requisitos(curriculo["texto"])

    print("\n" + "=" * 60)
    print(f"ARQUIVO: {curriculo['arquivo']}")
    print("=" * 60)

    if resultado["aprovado"]:

        print("STATUS: APROVADO")
        print("\nEnviando currículo para análise da IA...")

        try:
            analise = analisar_curriculo(curriculo["texto"])

            print("\nANÁLISE DA IA:")
            print(analise)

        except Exception as erro:
            print(f"\nErro ao analisar com a IA: {erro}")

    else:

        print("STATUS: REPROVADO")

        print("\nMotivos:")
        for motivo in resultado["motivos"]:
            print(f"- {motivo}")