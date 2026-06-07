# -*- coding: utf-8 -*-
"""Classificação de sistemas em tempo discreto.

Um **sistema** aqui é um operador ``sistema(x) -> y`` que recebe um sinal
(array NumPy 1-D) e devolve outro sinal de mesmo comprimento. As funções abaixo
decidem numericamente propriedades clássicas — linearidade, invariância no
tempo, causalidade e memória — por *sondagem*: aplicam o sistema a sinais de
prova e observam como a saída reage.

São versões limpas e verificáveis das funções exploradas no notebook
``02-classificacao-sistemas.ipynb``.
"""
from __future__ import annotations

import numpy as np

__all__ = [
    "deslocar",
    "eh_linear",
    "eh_invariante_no_tempo",
    "eh_causal",
    "tem_memoria",
]


def deslocar(x, k):
    """Desloca o sinal ``x`` por ``k`` amostras, preenchendo com zeros.

    ``k > 0`` atrasa (``y[n] = x[n-k]``); ``k < 0`` adianta.
    """
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    n = len(x)
    if k == 0:
        return x.copy()
    if k > 0:
        if k < n:
            y[k:] = x[: n - k]
    else:
        if -k < n:
            y[: n + k] = x[-k:]
    return y


def eh_linear(sistema, x1=None, x2=None, a=2.0, b=-3.0, tol=1e-9, n=32, seed=0):
    """Testa a linearidade (superposição) de ``sistema``.

    Verifica se ``T{a·x1 + b·x2} == a·T{x1} + b·T{x2}`` dentro de ``tol``.
    Se ``x1``/``x2`` não forem dados, usa ruído reprodutível (``seed``).
    """
    rng = np.random.default_rng(seed)
    if x1 is None:
        x1 = rng.standard_normal(n)
    if x2 is None:
        x2 = rng.standard_normal(n)
    x1 = np.asarray(x1, dtype=float)
    x2 = np.asarray(x2, dtype=float)
    lhs = np.asarray(sistema(a * x1 + b * x2), dtype=float)
    rhs = a * np.asarray(sistema(x1), dtype=float) + b * np.asarray(sistema(x2), dtype=float)
    return bool(np.allclose(lhs, rhs, atol=tol))


def eh_invariante_no_tempo(sistema, x=None, k=1, tol=1e-9, n=64, margem=8, seed=0):
    """Testa a invariância no tempo de ``sistema``.

    Verifica se atrasar a entrada equivale a atrasar a saída:
    ``T{x(n-k)} == (T{x})(n-k)``.

    Como o sinal é finito (com zero-padding nas bordas), usa uma entrada de
    **suporte compacto** — ruído confinado ao centro, zeros nas extremidades —
    e compara apenas o miolo, descartando ``margem`` amostras de cada lado.
    Isso elimina os artefatos de borda. Pressupõe sistemas de alcance finito
    menor que ``margem``.
    """
    rng = np.random.default_rng(seed)
    if x is None:
        x = np.zeros(n)
        x[2 * margem: n - 2 * margem] = rng.standard_normal(n - 4 * margem)
    x = np.asarray(x, dtype=float)
    lhs = np.asarray(sistema(deslocar(x, k)), dtype=float)
    rhs = deslocar(np.asarray(sistema(x), dtype=float), k)
    sl = slice(margem, len(x) - margem)
    return bool(np.allclose(lhs[sl], rhs[sl], atol=tol))


def eh_causal(sistema, n=24, tol=1e-9, seed=0):
    """Testa a causalidade de ``sistema``.

    Um sistema é causal quando a saída em um instante não depende de entradas
    *futuras*. Perturba a entrada apenas em índices ``> m`` e confere que a
    saída até ``m`` permanece inalterada.
    """
    rng = np.random.default_rng(seed)
    base = rng.standard_normal(n)
    y_base = np.asarray(sistema(base), dtype=float)
    for m in range(n - 1):
        x_mod = base.copy()
        x_mod[m + 1:] += rng.standard_normal(n - (m + 1))
        y_mod = np.asarray(sistema(x_mod), dtype=float)
        if not np.allclose(y_base[: m + 1], y_mod[: m + 1], atol=tol):
            return False  # mexer no futuro alterou o passado/presente -> não causal
    return True


def tem_memoria(sistema, n=24, tol=1e-9, seed=0):
    """Testa se ``sistema`` tem memória.

    Um sistema é *sem memória* quando ``y[k]`` depende apenas de ``x[k]``.
    Perturba uma amostra ``m`` e verifica se alguma saída em índice ``!= m``
    muda — se mudar, o sistema tem memória.
    """
    rng = np.random.default_rng(seed)
    base = rng.standard_normal(n)
    y_base = np.asarray(sistema(base), dtype=float)
    for m in range(n):
        x_mod = base.copy()
        x_mod[m] += 1.0
        y_mod = np.asarray(sistema(x_mod), dtype=float)
        diff = np.abs(y_mod - y_base)
        diff[m] = 0.0  # ignora o próprio índice perturbado
        if np.any(diff > tol):
            return True
    return False
