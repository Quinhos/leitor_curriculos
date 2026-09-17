from pypdf import PdfReader

def extrair_texto(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    paginas = []

    for pagina in reader.pages:
        texto = pagina.extract_text() or ""
        paginas.append(texto.strip())

    return "\n".join(paginas).strip()
