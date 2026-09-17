from pathlib import Path
from pypdf import PdfReader


def extrair_texto_pdf(caminho_pdf):
    """
    Extrai todo o texto de um arquivo PDF.
    """

    leitor = PdfReader(caminho_pdf)

    texto = ""

    for pagina in leitor.pages:
        conteudo = pagina.extract_text()

        if conteudo:
            texto += conteudo + "\n"

    return texto


def ler_curriculos(pasta="curriculos"):


    caminho_pasta = Path(pasta)

    curriculos = []

    for arquivo in caminho_pasta.glob("*.pdf"):

        try:
            texto = extrair_texto_pdf(arquivo)

            curriculos.append({
                "arquivo": arquivo.name,
                "caminho": str(arquivo),
                "texto": texto
            })

        except Exception as erro:
            print(f"Erro ao ler {arquivo.name}: {erro}")

    return curriculos