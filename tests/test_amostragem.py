# -*- coding: utf-8 -*-
"""Testes das utilidades de amostragem e aliasing."""
import numpy as np
import pytest

from sinais.amostragem import (
    frequencia_nyquist,
    satisfaz_nyquist,
    freq_aparente,
    reconstrucao_sinc,
)


def test_frequencia_nyquist():
    assert frequencia_nyquist(100) == 50.0


@pytest.mark.parametrize("f_max, fs, esperado", [
    (40, 100, True),
    (60, 100, False),
    (50, 100, True),   # fronteira fs == 2*f_max
])
def test_satisfaz_nyquist(f_max, fs, esperado):
    assert satisfaz_nyquist(f_max, fs) is esperado


@pytest.mark.parametrize("f, fs, alias", [
    (5, 50, 5),     # abaixo de Nyquist: sem alias
    (18, 20, 2),    # acima de Nyquist: dobra para 2 Hz
    (2, 20, 2),     # o "verdadeiro" 2 Hz
    (22, 20, 2),    # 22 -> |22 - 20| = 2 Hz
])
def test_freq_aparente_escalar(f, fs, alias):
    assert freq_aparente(f, fs) == pytest.approx(alias)


def test_freq_aparente_vetorizada():
    f = np.array([5, 18, 22])
    out = freq_aparente(f, 20)
    assert np.allclose(out, [5, 2, 2])
    # o alias está sempre dentro de [0, fs/2]
    assert np.all(out <= frequencia_nyquist(20))


def test_18_e_2_hz_indistinguiveis_apos_amostrar():
    fs = 20
    n = np.arange(0, 21)
    a = np.cos(2 * np.pi * 18 * n / fs)
    b = np.cos(2 * np.pi * 2 * n / fs)
    assert np.allclose(a, b)


def test_reconstrucao_exata_nos_instantes_de_amostragem():
    # nos próprios instantes nT, sinc(m-n) é um delta -> recupera a amostra
    fs, f = 20, 3
    n = np.arange(64)
    amostras = np.sin(2 * np.pi * f * n / fs)
    t = n / fs
    rec = reconstrucao_sinc(amostras, fs, t)
    assert np.allclose(rec, amostras, atol=1e-6)


def test_reconstrucao_aproxima_o_sinal_no_miolo():
    # longe das bordas, a interpolação sinc aproxima bem o sinal contínuo
    fs, f = 20, 3
    n = np.arange(64)
    amostras = np.sin(2 * np.pi * f * n / fs)
    t = np.linspace(1.0, 2.0, 200)          # miolo, longe de 0 e ~3.2 s
    rec = reconstrucao_sinc(amostras, fs, t)
    ref = np.sin(2 * np.pi * f * t)
    assert np.max(np.abs(rec - ref)) < 0.05
