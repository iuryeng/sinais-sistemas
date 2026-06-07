# -*- coding: utf-8 -*-
"""Utilidades de amostragem e aliasing.

Versões reutilizáveis e testáveis das funções do notebook
``06-amostragem-aliasing.ipynb``.
"""
from __future__ import annotations

import numpy as np

__all__ = [
    "frequencia_nyquist",
    "satisfaz_nyquist",
    "freq_aparente",
    "reconstrucao_sinc",
]


def frequencia_nyquist(fs):
    """Frequência de Nyquist (metade da taxa de amostragem)."""
    return fs / 2.0


def satisfaz_nyquist(f_max, fs):
    """Retorna ``True`` se ``fs`` amostra sem aliasing um sinal de banda ``f_max``.

    Condição de Nyquist–Shannon: ``fs >= 2 * f_max``.
    """
    return fs >= 2.0 * f_max


def freq_aparente(f, fs):
    """Frequência aparente (alias), em ``[0, fs/2]``, de um tom de ``f`` Hz.

    Resulta do *dobramento*: ``|f - round(f/fs) * fs|``.
    """
    k = np.round(np.asarray(f, dtype=float) / fs)
    return np.abs(np.asarray(f, dtype=float) - k * fs)


def reconstrucao_sinc(amostras, fs, t):
    """Reconstrução de Whittaker–Shannon por interpolação *sinc*.

    ``x(t) = Σ x[n] · sinc((t - n·T) / T)``, com ``T = 1/fs``.
    """
    amostras = np.asarray(amostras, dtype=float)
    t = np.asarray(t, dtype=float)
    ts = 1.0 / fs
    n = np.arange(len(amostras))
    # matriz (len(t) x len(n)) de sincs deslocadas, depois pondera e soma
    base = np.sinc((t[:, None] - n[None, :] * ts) / ts)
    return base @ amostras
