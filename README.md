# Sinais e Sistemas com Python

[![CI](https://github.com/iuryeng/sinais-sistemas/actions/workflows/ci.yml/badge.svg)](https://github.com/iuryeng/sinais-sistemas/actions/workflows/ci.yml)
[![JupyterLite](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://iuryeng.github.io/sinais-sistemas/)

> ▶️ **Rode no navegador, sem instalar nada:**
> **[sinais-sistemas interativo](https://iuryeng.github.io/sinais-sistemas/)** — os
> notebooks executam direto no browser (JupyterLite + Pyodide), até no celular.

Estudo prático de **Sinais e Sistemas** usando Python, NumPy, SciPy e Matplotlib.
Cada notebook explora um tópico da disciplina combinando teoria (definições,
fórmulas) com implementação e visualização computacional.

> Autor: **Iury Coelho** · Material de estudo / acadêmico

## Conteúdo

Os notebooks estão em [`notebooks/`](notebooks/) e foram pensados para serem
percorridos em ordem:

| # | Notebook | Tema |
|---|----------|------|
| 01 | [`01-sinais-elementares.ipynb`](notebooks/01-sinais-elementares.ipynb) | Geração de sinais elementares contínuos e discretos; impacto da amostragem na resolução e no tempo de processamento. |
| 02 | [`02-classificacao-sistemas.ipynb`](notebooks/02-classificacao-sistemas.ipynb) | Classificação de sistemas — linearidade, causalidade, memória e invariância no tempo — e introdução à convolução. |
| 03 | [`03-analise-sinais-sonoros.ipynb`](notebooks/03-analise-sinais-sonoros.ipynb) | Análise de sinais sonoros: harmônicos e conteúdo espectral de amostras de áudio. |
| 04 | [`04-transformada-fourier.ipynb`](notebooks/04-transformada-fourier.ipynb) | Transformada de Fourier — exemplos resolvidos (módulo, fase e espectro) na linha do Oppenheim. |
| 05 | [`05-convolucao-rir.ipynb`](notebooks/05-convolucao-rir.ipynb) | Convolução de um sinal de áudio com a resposta ao impulso de uma sala (auralização). *Material de terceiros — ver Créditos.* |
| 06 | [`06-amostragem-aliasing.ipynb`](notebooks/06-amostragem-aliasing.ipynb) | Amostragem, Teorema de Nyquist–Shannon, aliasing e dobramento espectral, reconstrução por interpolação *sinc* e um exemplo audível de aliasing. |
| 07 | [`07-filtros-digitais.ipynb`](notebooks/07-filtros-digitais.ipynb) | Filtros FIR e IIR (Butterworth): resposta em frequência, projeto com SciPy, FIR × IIR, remoção de ruído e filtragem de áudio (passa-banda). |

## Estrutura do projeto

```
sinais-sistemas/
├── notebooks/            # os notebooks, numerados na ordem de estudo
├── src/sinais/          # pacote Python reutilizável (funções testadas)
├── tests/               # testes pytest do pacote
├── assets/
│   └── images/          # figuras usadas/geradas pelos notebooks
├── tools/               # utilitários de manutenção/geração
├── .github/workflows/   # CI (testes + execução dos notebooks)
├── requirements.txt     # dependências dos notebooks
├── requirements-dev.txt # dependências de teste/CI
├── pyproject.toml       # configuração do pytest
├── LICENSE
└── README.md
```

## Rode no navegador (sem instalar)

A forma mais rápida de experimentar: abra
**<https://iuryeng.github.io/sinais-sistemas/>**. O site roda um JupyterLab
completo **dentro do navegador** (JupyterLite + Pyodide/WebAssembly) — você edita
e executa os notebooks sem instalar Python nem nada, até no celular.

> No navegador, o download de áudio por URL pode ser bloqueado pelo sandbox do
> Pyodide; nesse caso os notebooks caem automaticamente no *fallback* sintético.
> Para a experiência completa (com áudio real), rode localmente — veja abaixo.

## Como executar (localmente)

Pré-requisito: **Python 3.10+**.

```bash
# 1. clonar
git clone https://github.com/iuryeng/sinais-sistemas.git
cd sinais-sistemas

# 2. ambiente virtual (recomendado)
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# 3. dependências
pip install -r requirements.txt

# 4. abrir os notebooks
jupyter notebook   # ou: jupyter lab
```

### Sobre as amostras de áudio

Os notebooks de áudio (02, 03 e 05) **baixam as amostras por URL em tempo de
execução** (fonte estável: `pyroomacoustics`/LCAV), em vez de versionar arquivos
`.wav`. O carregamento tem **fallback sintético**: se não houver internet (ou a
URL falhar), uma célula gera um sinal equivalente, então os notebooks rodam do
zero em qualquer ambiente. O notebook 05 ainda sintetiza a resposta ao impulso
de sala (RIR) em código. Nada de áudio precisa ser versionado.

## Pacote `sinais` e testes

Funções centrais foram extraídas dos notebooks para um pacote reutilizável e
**testado** em [`src/sinais/`](src/sinais):

- `sinais.sistemas` — classificação de sistemas em tempo discreto
  (`eh_linear`, `eh_invariante_no_tempo`, `eh_causal`, `tem_memoria`), por
  sondagem numérica.
- `sinais.amostragem` — `frequencia_nyquist`, `satisfaz_nyquist`,
  `freq_aparente` (aliasing) e `reconstrucao_sinc` (Whittaker–Shannon).

Para rodar os testes:

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

A cada push/PR, o [workflow de CI](.github/workflows/ci.yml) instala as
dependências, roda o `pytest` e **executa os notebooks autocontidos**
(01, 02, 03, 05, 06 e 07) para garantir que não quebram. O notebook 04 fica de
fora por um bug pré-existente (o exemplo 8.8 chama `func_original8`, que nunca é
definido) — follow-up à parte.

## Bibliotecas utilizadas

- [NumPy](https://numpy.org/) — vetorização e operações numéricas
- [SciPy](https://scipy.org/) — `scipy.signal`, `scipy.io.wavfile`
- [Matplotlib](https://matplotlib.org/) — gráficos
- [ipywidgets](https://ipywidgets.readthedocs.io/) — controles interativos
- [Requests](https://requests.readthedocs.io/) — download das amostras de áudio

## Créditos

O notebook **05 — Convolução com RIR** é derivado de material educacional aberto
(Open Educational Resources) do curso *"Selected Topics in Audio Signal
Processing"*, distribuído sob CC BY 4.0 (texto) e MIT (código). O crédito é dos
autores originais; aqui ele é mantido para fins de estudo.

## Licença

Código autoral deste repositório sob [MIT](LICENSE). Material de terceiros (ver
Créditos) mantém a licença original.
