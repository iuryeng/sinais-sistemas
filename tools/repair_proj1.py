"""Repara proj_1sinais_sistemas.ipynb (JSON truncado no meio de um output base64).

Estrategia: parsear o array "cells" objeto-a-objeto com JSONDecoder.raw_decode,
descartando a primeira celula que falhar (a truncada) e tudo apos ela.
Reconstroi um notebook nbformat 4 valido com as celulas recuperadas.
"""
import json
import os

ROOT = r"C:\Users\Iury Coelho\projetos\sinais-sistemas"
SRC = os.path.join(ROOT, "proj_1sinais_sistemas.ipynb")
OUT = os.path.join(ROOT, "proj_1sinais_sistemas.repaired.ipynb")

with open(SRC, encoding="utf-8") as f:
    text = f.read()

# Localiza o inicio do array de celulas
key = '"cells"'
ki = text.find(key)
lb = text.find("[", ki)
idx = lb + 1

dec = json.JSONDecoder()
cells = []
n_ok = 0
while True:
    # pula espacos e virgulas entre objetos
    while idx < len(text) and text[idx] in " \t\r\n,":
        idx += 1
    if idx >= len(text) or text[idx] == "]":
        break
    try:
        obj, end = dec.raw_decode(text, idx)
    except json.JSONDecodeError as e:
        print(f"Celula {n_ok+1}: parse falhou em char {idx} ({e.msg}). "
              f"Descartando esta e o restante.")
        break
    cells.append(obj)
    n_ok += 1
    idx = end

# Sanitiza: garante campos minimos por celula e limpa outputs quebrados
clean = []
for c in cells:
    ct = c.get("cell_type")
    if ct not in ("code", "markdown", "raw"):
        continue
    c.setdefault("metadata", {})
    if ct == "code":
        c.setdefault("outputs", [])
        c.setdefault("execution_count", None)
    clean.append(c)

nb = {
    "cells": clean,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

n_md = sum(1 for c in clean if c["cell_type"] == "markdown")
n_code = sum(1 for c in clean if c["cell_type"] == "code")
print(f"Recuperadas {len(clean)} celulas (markdown: {n_md}, code: {n_code})")
print(f"Salvo em: {OUT}")
