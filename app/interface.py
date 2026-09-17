import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from app.filtros import aplicar_filtros
from app.ia import analisar_curriculo
from app.pdf_reader import extrair_texto
from app.relatorio import gerar_relatorio


load_dotenv()

# CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="Tech Talent AI",
    page_icon="💼",
    layout="wide"
)


# CABEÇALHO

st.title("Tech Talent AI")

st.subheader(
    "Triagem inteligente de currículos"
)

st.write(
    "Sistema de triagem automatizada para "
    "profissionais do ecossistema de tecnologia."
)

st.divider()


# CONFIGURAÇÕES DA VAGA

st.header("Configuração da vaga")

coluna1, coluna2 = st.columns(2)


with coluna1:

    experiencia_minima = st.number_input(
        "Experiência mínima (anos)",
        min_value=0.0,
        value=2.0,
        step=0.5
    )


with coluna2:

    salario_maximo = st.number_input(
        "Orçamento máximo da vaga (R$)",
        min_value=0.0,
        value=8000.0,
        step=500.0
    )


# UPLOAD DO CURRÍCULO

st.header("Currículo")

arquivo = st.file_uploader(
    "Envie o currículo em formato PDF",
    type=["pdf"]
)


# BOTÃO DE ANÁLISE

if arquivo:

    if st.button(
        "ANALISAR CURRÍCULO",
        use_container_width=True
    ):

        # Criamos um arquivo temporário
        # para que o pypdf consiga lê-lo.
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as arquivo_temporario:

            arquivo_temporario.write(
                arquivo.getvalue()
            )

            caminho_pdf = arquivo_temporario.name


        try:

            # 1 - EXTRAÇÃO DO PDF

            texto = extrair_texto(
                caminho_pdf
            )


            if not texto:

                st.error(
                    "Não foi possível extrair "
                    "texto do currículo."
                )

                st.stop()

            # 2 - FILTROS DETERMINÍSTICOS

            filtros = aplicar_filtros(

                texto,

                experiencia_minima,

                salario_maximo
            )


            st.divider()

            st.header(
                "Resultado da triagem"
            )

            # RESULTADO

            if filtros["aprovado"]:

                st.success(
                    "CANDIDATO APROVADO "
                    "PARA ANÁLISE DE IA"
                )

            else:

                st.error(
                    "CANDIDATO REPROVADO "
                    "NOS FILTROS"
                )

            # INDICADORES
            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Experiência",
                    f"{filtros['experiencia']:.1f} anos"
                )


            with col2:

                if filtros["salario"]:

                    salario_formatado = (
                        f"R$ {filtros['salario']:,.2f}"
                    )

                else:

                    salario_formatado = (
                        "Não identificada"
                    )


                st.metric(
                    "Pretensão salarial",
                    salario_formatado
                )


            with col3:

                st.metric(
                    "Status",
                    (
                        "APROVADO"
                        if filtros["aprovado"]
                        else "REPROVADO"
                    )
                )

            # DETALHAMENTO DOS FILTROS

            st.subheader(
                "Filtros determinísticos"
            )


            if filtros["experiencia_ok"]:

                st.write(
                    "Experiência mínima: OK"
                )

            else:

                st.write(
                    "Experiência mínima: "
                    "NÃO ATENDIDA"
                )


            if filtros["salario_ok"]:

                st.write(
                    "Faixa salarial: OK"
                )

            else:

                st.write(
                    "Faixa salarial: "
                    "INCOMPATÍVEL"
                )


            # 3 - IA GENERATIVA

            analise = None


            if filtros["aprovado"]:

                if not os.getenv(
                    "OPENAI_API_KEY"
                ):

                    st.warning(
                        "O candidato foi aprovado, "
                        "mas a OPENAI_API_KEY não "
                        "está configurada no .env."
                    )

                else:

                    modelo = os.getenv(
                        "OPENAI_MODEL",
                        "gpt-4o-mini"
                    )


                    with st.spinner(
                        "Executando análise generativa..."
                    ):

                        analise = analisar_curriculo(
                            texto,
                            modelo
                        )

                    # PARECER
                    

                    st.divider()

                    st.header(
                        "Análise generativa"
                    )

                    st.write(
                        analise["texto"]
                    )


                    
                    # TOKENS
                    

                    st.subheader(
                        "Monitoramento de tokens"
                    )


                    token1, token2, token3, token4 = (
                        st.columns(4)
                    )


                    with token1:

                        st.metric(
                            "Tokens de entrada",
                            analise["prompt_tokens"]
                        )


                    with token2:

                        st.metric(
                            "Tokens de saída",
                            analise["completion_tokens"]
                        )


                    with token3:

                        st.metric(
                            "Tokens totais",
                            analise["total_tokens"]
                        )


                    with token4:

                        st.metric(
                            "Custo estimado",
                            (
                                "US$ "
                                f"{analise['custo_estimado']:.6f}"
                            )
                        )


            # 4 - RELATÓRIO

            relatorio = gerar_relatorio(

                arquivo.name,

                filtros,

                analise
            )


            st.divider()

            st.header(
                "Relatório da triagem"
            )


            with open(
                relatorio,
                "rb"
            ) as arquivo_relatorio:

                st.download_button(

                    label="BAIXAR RELATÓRIO",

                    data=arquivo_relatorio.read(),

                    file_name=relatorio.name,

                    mime="text/plain",

                    use_container_width=True
                )


        finally:

            # Remove o arquivo temporário.
            try:

                os.remove(
                    caminho_pdf
                )

            except OSError:

                pass


# RODAPÉ

st.divider()

st.caption(
    "Projeto acadêmico - Engenharia de Software "
    "- IA & ML - 3ESPA"
)