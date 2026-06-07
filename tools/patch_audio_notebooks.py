# -*- coding: utf-8 -*-
"""Torna os notebooks 02/03/05 autocontidos: amostras de áudio baixadas por URL
em runtime (com fallback sintético), reconstruindo as seções quebradas.

Idempotente para o nb02 (mantém o markdown "## Convolução" e substitui tudo
após ele). Para 03/05, localiza células por substring do conteúdo original;
rode sobre o estado base (git checkout antes de re-rodar)."""
import os
import nbformat
from nbformat.v4 import new_markdown_cell, new_code_cell

NBDIR = r"C:\Users\Iury Coelho\projetos\sinais-sistemas\notebooks"
BASE = "https://raw.githubusercontent.com/LCAV/pyroomacoustics/master/examples/input_samples/"
URL_FALA = BASE + "cmu_arctic_us_aew_a0001.wav"


def C(s):
    return new_code_cell(s.strip("\n"))


def M(s):
    return new_markdown_cell(s.strip("\n"))


def find(cells, substr, kind=None):
    for i, c in enumerate(cells):
        if (kind is None or c.cell_type == kind) and substr in "".join(c.source):
            return i
    raise ValueError("não encontrei célula com: " + substr)


def save(nb, path):
    nb.nbformat_minor = 5          # permite o campo 'id' nas células
    _, nb = nbformat.validator.normalize(nb)
    nbformat.write(nb, path)


HELPER_FALA = '''
import requests, io
from scipy.io import wavfile
from IPython.display import Audio, display

def carregar_wav(url, fallback_fs=16000, fallback_dur=3.0, timeout=20):
    # Baixa um .wav por URL (notebook autocontido). Se a rede/URL falhar,
    # gera um sinal sintetico para rodar do zero em qualquer ambiente (ex.: CI).
    try:
        R = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        R.raise_for_status()
        fs, data = wavfile.read(io.BytesIO(R.content))
        data = np.asarray(data, dtype=float)
        if data.ndim > 1:
            data = data[:, 0]
        return data / (np.max(np.abs(data)) or 1.0), int(fs)
    except Exception as e:
        print(f"[aviso] download falhou ({type(e).__name__}); usando sinal sintetico.")
        fs = fallback_fs
        t = np.linspace(0, fallback_dur, int(fs * fallback_dur), endpoint=False)
        voz = sum((1.0 / k) * np.sin(2 * np.pi * 150 * k * t) for k in range(1, 8))
        voz *= 0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 2.5 * t))
        return voz / np.max(np.abs(voz)), fs
'''

# ============================ nb05 ============================
p = os.path.join(NBDIR, "05-convolucao-rir.ipynb")
nb = nbformat.read(p, as_version=4)
cells = nb.cells

cells[find(cells, "sf.read('speech.wav')")] = C(
    "%matplotlib inline\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "import scipy.signal as sig\n"
    + HELPER_FALA.strip("\n") + "\n\n"
    'URL_FALA = "' + URL_FALA + '"\n'
    "x, fs = carregar_wav(URL_FALA)"
)

cells[find(cells, "sf.read('room_impulse_response.wav')")] = C('''
# Resposta ao impulso de sala (RIR) sintetica: som direto + reflexoes iniciais
# + cauda reverberante com decaimento exponencial. Substitui um .wav de RIR,
# mantendo o notebook autocontido.
fsh = fs
dur_rir = 0.4
n = int(dur_rir * fsh)
t_rir = np.arange(n) / fsh
rng = np.random.default_rng(0)
h = rng.standard_normal(n) * np.exp(-7.0 * t_rir)
h[0] = 1.0
for atraso, ganho in [(0.011, 0.6), (0.019, 0.4), (0.031, 0.3), (0.043, 0.2)]:
    i = int(atraso * fsh)
    if i < n:
        h[i] += ganho
h = h / np.max(np.abs(h))
''')

cells[find(cells, "sf.write('dry_source.wav'")] = C('''
# Auralizacao: normaliza e ouve o sinal seco (entrada) e o molhado (com sala).
seco = x / np.max(np.abs(x))
molhado = y / np.max(np.abs(y))
print("Sinal seco (sem sala):")
display(Audio(seco, rate=fs))
print("Sinal com a sala (convoluido com a RIR):")
display(Audio(molhado, rate=fs))
''')

cells[find(cells, '<audio src="dry_source.wav"')] = M(
    "**Sinal seco (sem sala)** — reproduzido na célula acima (entrada $x[k]$)."
)
cells[find(cells, '<audio src="wet_source.wav"')] = M(
    "**Sinal com a sala (reverberação)** — reproduzido na célula acima (saída $y[k]$)."
)
save(nb, p)
print("nb05 OK")

# ============================ nb02 ============================
p = os.path.join(NBDIR, "02-classificacao-sistemas.ipynb")
nb = nbformat.read(p, as_version=4)
cells = nb.cells

# corrige bug pre-existente: a celula chama verifyMemory, mas a funcao e hasMemory
for c in cells:
    if c.cell_type == "code" and "verifyMemory(" in "".join(c.source):
        c.source = "".join(c.source).replace("verifyMemory(", "hasMemory(")

# remove a dependencia de soundfile (nao usada apos o patch)
i_imp = find(cells, "import soundfile as sf")
cells[i_imp].source = "".join(
    ln for ln in cells[i_imp].source.splitlines(keepends=True)
    if "import soundfile as sf" not in ln
).rstrip() + "\n"

# trunca tudo apos "## Convolução" e reconstroi a secao
corte = find(cells, "## Convolução", kind="markdown") + 1
nova = [
    M("Para ilustrar a **convolução**, carregamos um sinal de fala real "
      "(baixado por URL) e o processamos com um sistema LTI cuja resposta ao "
      "impulso produz um **eco**."),
    C("import requests, io\n"
      "from scipy.io import wavfile\n"
      "from IPython.display import Audio, display\n"
      + HELPER_FALA.split('from IPython.display import Audio, display\n', 1)[1].strip("\n")
      + "\n\n"
      'URL_FALA = "' + URL_FALA + '"\n'
      "x, fs = carregar_wav(URL_FALA)"),
    C('''
plt.figure(figsize=(8, 3.5))
t = np.arange(len(x)) / fs
plt.plot(t, x)
plt.grid(alpha=.3); plt.xlabel('t [s]'); plt.ylabel('x(t)')
plt.title('Sinal de fala (entrada)')
plt.show()
'''),
    M(r"A resposta ao impulso de um **eco** é um impulso direto somado a uma "
      r"cópia atrasada e atenuada: $h[k] = \delta[k] + a\,\delta[k - D]$."),
    C('''
# Eco: impulso direto + copia atrasada (D amostras) e atenuada (ganho a).
atraso, a = 0.25, 0.6
h = np.zeros(int((atraso + 0.02) * fs))
h[0] = 1.0
h[int(atraso * fs)] = a

plt.figure(figsize=(8, 3))
th = np.arange(len(h)) / fs
plt.plot(th, h)
plt.grid(alpha=.3); plt.xlabel('t [s]'); plt.ylabel('h(t)')
plt.title(f'Resposta ao impulso do eco (atraso {atraso}s, ganho {a})')
plt.show()
'''),
    M(r"A saída é a **convolução** $y = x * h$, que aplica o eco ao sinal de fala."),
    C('''
y = np.convolve(x, h)
plt.figure(figsize=(8, 3.5))
ty = np.arange(len(y)) / fs
plt.plot(ty, y)
plt.grid(alpha=.3); plt.xlabel('t [s]'); plt.ylabel('y(t)')
plt.title('Saída y = x * h (sinal com eco)')
plt.show()
'''),
    M("### Auralização — ouça a diferença"),
    C('''
print("Entrada (sem eco):")
display(Audio(x, rate=fs))
print("Saída (com eco):")
display(Audio(y / np.max(np.abs(y)), rate=fs))
'''),
]
nb.cells = cells[:corte] + nova
save(nb, p)
print("nb02 OK")

# ============================ nb03 ============================
p = os.path.join(NBDIR, "03-analise-sinais-sonoros.ipynb")
nb = nbformat.read(p, as_version=4)
cells = nb.cells

corte = find(cells, "Considerações", kind="markdown")  # MD logo antes do loadSound
nova = [
    M("As amostras de áudio são **baixadas por URL** de uma fonte estável "
      "(pyroomacoustics / LCAV). O carregamento tem *fallback* sintético, então "
      "o notebook roda do zero mesmo sem internet."),
    C('''
def loadSound(url, fallback_f0=220, fallback_fs=8000, fallback_dur=2.0, timeout=20):
    # Baixa um .wav por URL e normaliza para [-1, 1] (mono). Se falhar, gera um
    # tom harmonico sintetico para o notebook rodar do zero (ex.: no CI).
    try:
        R = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        R.raise_for_status()
        rate, data = wavfile.read(BytesIO(R.content))
        data = np.asarray(data, dtype=float)
        if data.ndim > 1:
            data = data[:, 0]
        return data / (np.abs(data).max() or 1.0), int(rate)
    except Exception as e:
        print(f"[aviso] download falhou ({type(e).__name__}); usando tom sintetico.")
        fs = fallback_fs
        t = np.linspace(0, fallback_dur, int(fs * fallback_dur), endpoint=False)
        s = sum((1.0 / k) * np.sin(2 * np.pi * fallback_f0 * k * t) for k in range(1, 10))
        return s / np.abs(s).max(), fs

BASE = "''' + BASE + '''"
SONS = [
    ("Canto (rico em harmônicos)", BASE + "singing_8000.wav"),
    ("Voz masculina", BASE + "cmu_arctic_us_aew_a0001.wav"),
    ("Voz feminina", BASE + "cmu_arctic_us_axb_a0004.wav"),
]

def mostrar_som(nome, url):
    x, fs = loadSound(url)
    t = np.arange(len(x)) / fs
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3))
    a1.plot(t, x); a1.set_title(nome + " — forma de onda")
    a1.set_xlabel("t [s]"); a1.grid(alpha=.3)
    meio = len(x) // 2
    jan = slice(meio, meio + int(0.05 * fs))   # zoom de 50 ms no meio
    a2.plot(t[jan], x[jan]); a2.set_title("zoom (50 ms) — periodicidade")
    a2.set_xlabel("t [s]"); a2.grid(alpha=.3)
    plt.tight_layout(); plt.show()
    display(Audio(x, rate=fs))
    return x, fs
'''),
    M("### 1ª amostra — canto"),
    C("x1, fs1 = mostrar_som(*SONS[0])"),
    M("### 2ª amostra — voz masculina"),
    C("x2, fs2 = mostrar_som(*SONS[1])"),
    M("### 3ª amostra — voz feminina"),
    C("x3, fs3 = mostrar_som(*SONS[2])"),
    M("## Análise espectral — os harmônicos\n\nA Transformada de Fourier revela "
      "o conteúdo harmônico do som. No canto, os picos aparecem em múltiplos "
      "(harmônicos) da frequência fundamental."),
    C('''
X = np.abs(np.fft.rfft(x1))
f = np.fft.rfftfreq(len(x1), 1 / fs1)
plt.figure(figsize=(9, 3.2))
plt.plot(f, X)
plt.xlim(0, 2000)
plt.grid(alpha=.3); plt.xlabel("frequência [Hz]"); plt.ylabel("|X(f)|")
plt.title("Espectro do canto — picos nos harmônicos")
plt.show()
'''),
]
nb.cells = cells[:corte] + nova
save(nb, p)
print("nb03 OK")
print("\nconcluido.")
