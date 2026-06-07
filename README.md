# Sinais e Sistemas com Python

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

## Estrutura do projeto

```
sinais-sistemas/
├── notebooks/        # os notebooks, numerados na ordem de estudo
├── assets/
│   └── images/       # figuras usadas/geradas pelos notebooks
├── tools/            # utilitários de manutenção do repositório
├── requirements.txt  # dependências Python
├── LICENSE
└── README.md
```

## Como executar

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

Os notebooks de áudio (02, 03 e 05) usam amostras de som. Para manter o
repositório leve e autocontido, a estratégia é **baixar as amostras por URL em
tempo de execução** (a própria célula faz o download), em vez de versionar os
arquivos `.wav`. Os áudios baixados/gerados ficam fora do controle de versão
(ver `.gitignore`).

## Bibliotecas utilizadas

- [NumPy](https://numpy.org/) — vetorização e operações numéricas
- [SciPy](https://scipy.org/) — `scipy.signal`, `scipy.io.wavfile`
- [Matplotlib](https://matplotlib.org/) — gráficos
- [SoundFile](https://python-soundfile.readthedocs.io/) — leitura/escrita de `.wav`
- [ipywidgets](https://ipywidgets.readthedocs.io/) — controles interativos
- [Requests](https://requests.readthedocs.io/) — download das amostras

## Créditos

O notebook **05 — Convolução com RIR** é derivado de material educacional aberto
(Open Educational Resources) do curso *"Selected Topics in Audio Signal
Processing"*, distribuído sob CC BY 4.0 (texto) e MIT (código). O crédito é dos
autores originais; aqui ele é mantido para fins de estudo.

## Licença

Código autoral deste repositório sob [MIT](LICENSE). Material de terceiros (ver
Créditos) mantém a licença original.
