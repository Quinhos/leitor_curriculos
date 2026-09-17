# Agência de Empregos Tech
 Nome: Marcos Santos / RM: 560062 <br>
 Nome: Davi Correia / RM: 560438

Projeto em Python para triagem automatizada de currículos de desenvolvedores em PDF.

## Fluxo

1. Extrai o texto do currículo em PDF.
2. Aplica filtros determinísticos:
   - experiência mínima;
   - compatibilidade salarial.
3. Somente candidatos aprovados seguem para a IA generativa.
4. A IA gera:
   - parecer qualitativo de senioridade e soft skills;
   - resumo executivo para o recrutador.
5. O sistema contabiliza tokens de entrada e saída e estima o custo.

## Instalação

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e informe sua chave da API.

## Execução

```bash
python -m app.main
```

Quando solicitado, informe o caminho do PDF e os dados da vaga.
