# Agência de Empregos Tech

Projeto em Python desenvolvido para uma agência de empregos focada no ecossistema de tecnologia.

O sistema automatiza a triagem de currículos em formato PDF, combinando filtros determinísticos de regras de negócio com análise qualitativa realizada por Inteligência Artificial Generativa.

A solução utiliza **DeepSeek-R1 executado localmente através do Ollama**, evitando a necessidade de uma API paga para a análise dos currículos.

---

## Integrantes

* **Marcos Santos** — RM: 560062
* **Davi Correia** — RM: 560438

### Repositório

https://github.com/Quinhos/leitor_curriculos

---

# Objetivo do Projeto

Desenvolver um sistema capaz de automatizar parte do processo de triagem de currículos de profissionais da área de tecnologia.

O sistema realiza inicialmente uma análise determinística, baseada em regras de negócio, antes de utilizar Inteligência Artificial.

Essa abordagem permite evitar o processamento desnecessário de currículos que não atendem aos requisitos mínimos da vaga.

Os candidatos aprovados pelos filtros determinísticos são encaminhados para análise qualitativa utilizando um modelo de linguagem executado localmente.

---

# Tecnologias Utilizadas

* Python
* PyPDF
* Ollama
* DeepSeek-R1
* Tiktoken
* python-dotenv
* Git
* GitHub
* Visual Studio Code

---

# Funcionamento do Sistema

O fluxo de processamento ocorre da seguinte forma:

```text
Currículo em PDF
       |
       v
Extração do texto
       |
       v
Filtros determinísticos
       |
       +-----------------------+
       |                       |
       v                       v
   Reprovado                Aprovado
       |                       |
       v                       v
Relatório               Inteligência Artificial
                               |
                               v
                         DeepSeek-R1
                               |
                 +-------------+-------------+
                 |             |             |
                 v             v             v
            Senioridade   Soft Skills   Resumo Executivo
                 |             |             |
                 +-------------+-------------+
                               |
                               v
                         Relatório final
                               |
                               v
                       Tokens e custo
```

---

# 1. Leitura e Extração dos Currículos

Os currículos devem ser disponibilizados em formato PDF dentro da pasta:

```text
curriculos/
```

O sistema utiliza a biblioteca **PyPDF** para abrir os arquivos e extrair o texto dos documentos.

Exemplo:

```text
curriculos/
├── curriculo1.pdf
├── curriculo2.pdf
└── curriculo3.pdf
```

Após a extração, o texto é encaminhado para a camada de filtros determinísticos.

---

# 2. Filtros Determinísticos

Antes de utilizar a Inteligência Artificial, o sistema aplica regras fixas de negócio.

Essa etapa tem como objetivo eliminar candidatos que não atendem aos requisitos mínimos da vaga antes de realizar o processamento generativo.

Atualmente são utilizados dois filtros obrigatórios.

## Experiência profissional

O sistema verifica o tempo de experiência informado no currículo.

Configuração atual:

```python
EXPERIENCIA_MINIMA_ANOS = 2
```

Candidatos com menos de 2 anos de experiência são reprovados.

---

## Pretensão salarial

O sistema também identifica a pretensão salarial do candidato e compara o valor com o orçamento máximo definido para a vaga.

Configuração atual:

```python
ORCAMENTO_MAXIMO = 5000.00
```

Candidatos com pretensão salarial superior a R$ 5.000,00 são reprovados.

---

## Exemplo

Um candidato com:

```text
Experiência: 4 anos
Pretensão salarial: R$ 4.500,00
```

é aprovado na etapa determinística.

Já um candidato com:

```text
Experiência: 1 ano
Pretensão salarial: R$ 4.000,00
```

é reprovado por não atingir o tempo mínimo de experiência.

Outro candidato com:

```text
Experiência: 5 anos
Pretensão salarial: R$ 7.000,00
```

é reprovado porque sua pretensão salarial ultrapassa o orçamento da vaga.

---

# 3. Análise com Inteligência Artificial

Somente os currículos aprovados na etapa determinística são enviados para a camada generativa.

O projeto utiliza o **DeepSeek-R1**, executado localmente através do **Ollama**.

A análise generativa produz:

* avaliação de senioridade;
* análise de soft skills;
* competências técnicas;
* experiências relevantes;
* pontos positivos;
* pontos a desenvolver;
* resumo executivo para o recrutador;
* parecer qualitativo sobre o perfil.

A análise é baseada exclusivamente nas informações extraídas do currículo.

O sistema instrui o modelo a não inventar experiências, tecnologias, certificações ou outras qualificações que não estejam presentes no documento.

---

# 4. Execução Local da IA

O modelo utilizado pelo projeto é:

```text
deepseek-r1:7b
```

O modelo é executado localmente através do Ollama.

Isso significa que o projeto não depende de uma chave da API da OpenAI para realizar a análise generativa.

O modelo utilizado pode ser configurado no arquivo:

```text
.env
```

Exemplo:

```env
OLLAMA_MODEL=deepseek-r1:7b
```

---

# 5. Monitoramento de Tokens

O projeto também realiza o monitoramento do consumo de tokens durante a análise generativa.

São registrados:

* tokens de entrada;
* tokens de saída;
* tokens totais;
* modelo utilizado;
* contagem complementar utilizando `tiktoken`;
* custo estimado da execução.

O Ollama fornece as informações de tokens utilizadas durante a execução do modelo.

O `tiktoken` também é utilizado como ferramenta complementar de contagem.

Como o modelo é executado localmente através do Ollama, não existe cobrança de API por token.

Por isso, o custo de API da execução local é considerado:

```text
R$ 0,00
```

---

# 6. Geração de Relatórios

Após o processamento, o sistema gera automaticamente um relatório em formato `.txt`.

Os relatórios são armazenados em:

```text
relatorios/
```

Exemplo:

```text
relatorios/
├── curriculo1_relatorio.txt
├── curriculo2_relatorio.txt
└── curriculo3_relatorio.txt
```

Os relatórios contêm informações como:

* arquivo analisado;
* data da análise;
* experiência identificada;
* experiência mínima exigida;
* pretensão salarial;
* orçamento da vaga;
* status da triagem;
* motivos da reprovação;
* análise da IA;
* modelo utilizado;
* tokens de entrada;
* tokens de saída;
* tokens totais;
* custo estimado.

---

# 7. Organização dos Currículos

Após a triagem, os arquivos são copiados automaticamente para suas respectivas pastas.

Currículos aprovados:

```text
aprovados/
```

Currículos reprovados:

```text
reprovados/
```

Exemplo:

```text
aprovados/
└── curriculo1.pdf

reprovados/
├── curriculo2.pdf
└── curriculo3.pdf
```

Os arquivos originais permanecem na pasta `curriculos/`.

---

# Estrutura do Projeto

```text
agencia_empregos_tech/
│
├── app/
│   ├── main.py
│   ├── pdf_reader.py
│   ├── filtros.py
│   ├── ia.py
│   └── relatorio.py
│
├── curriculos/
│   ├── curriculo1.pdf
│   ├── curriculo2.pdf
│   └── curriculo3.pdf
│
├── aprovados/
│   └── curriculo1.pdf
│
├── reprovados/
│   ├── curriculo2.pdf
│   └── curriculo3.pdf
│
├── relatorios/
│   └── relatórios gerados automaticamente
│
├── .env
├── .env.example
├── .gitignore
├── integrantes.txt
├── requirements.txt
└── README.md
```

---

# Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/Quinhos/leitor_curriculos.git
```

Entre na pasta do projeto:

```bash
cd leitor_curriculos
```

---

## 2. Criar ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\activate
```

---

## 3. Instalar as dependências

```powershell
pip install -r requirements.txt
```

---

# Configuração do Ollama

O Ollama precisa estar instalado no computador para executar o modelo localmente.

Depois da instalação, verifique:

```powershell
ollama --version
```

Baixe o modelo utilizado pelo projeto:

```powershell
ollama run deepseek-r1:7b
```

Após o download, o modelo estará disponível localmente para o sistema.

---

# Configuração do arquivo `.env`

Crie um arquivo chamado:

```text
.env
```

Na raiz do projeto.

Adicione:

```env
OLLAMA_MODEL=deepseek-r1:7b
```

O arquivo `.env` não deve ser enviado ao GitHub.

Por isso, ele está incluído no `.gitignore`.

O arquivo `.env.example` pode ser utilizado como modelo para a configuração.

---

# Execução

Com o ambiente virtual ativado:

```powershell
python app/main.py
```

O sistema irá:

1. localizar os currículos na pasta `curriculos`;
2. extrair o texto dos PDFs;
3. verificar os requisitos determinísticos;
4. reprovar candidatos que não atendam aos critérios;
5. enviar somente os aprovados para o DeepSeek;
6. gerar a análise qualitativa;
7. contabilizar os tokens;
8. gerar os relatórios;
9. organizar os currículos nas pastas `aprovados` e `reprovados`.

---

# Exemplo de Execução

```text
============================================================
AGÊNCIA DE EMPREGOS TECH
Sistema de Triagem Automatizada de Currículos
============================================================

Iniciando análise dos currículos...
Currículos encontrados: 3

============================================================
ARQUIVO: curriculo1.pdf
============================================================

Experiência identificada: 4 anos
Pretensão salarial: R$ 4.500,00

STATUS: APROVADO

Enviando currículo para análise da IA...

ANÁLISE DA IA:

SENIORIDADE
...

SOFT SKILLS
...

RESUMO EXECUTIVO
...

INFORMAÇÕES SOBRE TOKENS

Modelo: deepseek-r1:7b
Tokens de entrada: ...
Tokens de saída: ...
Tokens totais: ...
Custo estimado: R$ 0.00
```

Para um currículo que não atende aos requisitos:

```text
STATUS: REPROVADO

Motivos:
- Experiência insuficiente: 1 ano.
  Mínimo exigido: 2 anos.
```

Nesse caso, o currículo não é enviado para a Inteligência Artificial.

---

# Segurança

Informações sensíveis e configurações locais não devem ser versionadas no GitHub.

O projeto utiliza `.gitignore` para evitar o envio de arquivos como:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

# Controle de Versão

O desenvolvimento do projeto utiliza Git e GitHub.

Foram utilizados commits semânticos para organizar a evolução do sistema.

Exemplos:

```text
feat: implementa leitura de curriculos em PDF
feat: adiciona filtros determinísticos
feat: integra análise generativa
feat: implementa monitoramento de tokens
feat: adiciona geração de relatórios
docs: atualiza documentação do projeto
```

---

# Conclusão

O projeto apresenta uma solução automatizada para triagem de currículos voltada ao ecossistema de tecnologia.

A arquitetura combina regras determinísticas com Inteligência Artificial Generativa, permitindo que somente candidatos que atendam aos requisitos mínimos avancem para a análise qualitativa.

A utilização do Ollama com o DeepSeek-R1 permite executar a análise de forma local, enquanto o monitoramento de tokens possibilita acompanhar os recursos utilizados durante o processamento generativo.

O projeto também automatiza a geração de relatórios e a organização dos currículos de acordo com o resultado da triagem.

---

# Repositório

https://github.com/Quinhos/leitor_curriculos
