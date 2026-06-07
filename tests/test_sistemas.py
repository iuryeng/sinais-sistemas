# -*- coding: utf-8 -*-
"""Testes de classificação de sistemas com sistemas de prova conhecidos."""
import numpy as np
import pytest

from sinais.sistemas import (
    deslocar,
    eh_linear,
    eh_invariante_no_tempo,
    eh_causal,
    tem_memoria,
)

# --- sistemas de prova (operadores sinal -> sinal) -------------------------
ganho       = lambda x: 2.0 * x                       # linear, s/ mem, causal, invariante
afim        = lambda x: 2.0 * x + 1.0                 # NÃO-linear (afim)
quadrado    = lambda x: x ** 2                        # NÃO-linear
atraso1     = lambda x: deslocar(x, 1)                # y[n]=x[n-1]: c/ mem, causal
avanco1     = lambda x: deslocar(x, -1)               # y[n]=x[n+1]: c/ mem, NÃO-causal
variante    = lambda x: np.arange(len(x)) * x         # y[n]=n·x[n]: variante no tempo
media_movel = lambda x: (x + deslocar(x, 1)) / 2.0    # c/ mem, causal, invariante


# --- linearidade -----------------------------------------------------------
@pytest.mark.parametrize("sistema", [ganho, atraso1, avanco1, variante, media_movel])
def test_lineares(sistema):
    assert eh_linear(sistema) is True


@pytest.mark.parametrize("sistema", [afim, quadrado])
def test_nao_lineares(sistema):
    assert eh_linear(sistema) is False


# --- invariância no tempo --------------------------------------------------
@pytest.mark.parametrize("sistema", [ganho, quadrado, atraso1, avanco1, media_movel])
def test_invariantes_no_tempo(sistema):
    assert eh_invariante_no_tempo(sistema) is True


def test_variante_no_tempo():
    assert eh_invariante_no_tempo(variante) is False


# --- causalidade -----------------------------------------------------------
@pytest.mark.parametrize("sistema", [ganho, quadrado, atraso1, variante, media_movel])
def test_causais(sistema):
    assert eh_causal(sistema) is True


def test_nao_causal():
    assert eh_causal(avanco1) is False


# --- memória ---------------------------------------------------------------
@pytest.mark.parametrize("sistema", [atraso1, avanco1, media_movel])
def test_com_memoria(sistema):
    assert tem_memoria(sistema) is True


@pytest.mark.parametrize("sistema", [ganho, quadrado, variante])
def test_sem_memoria(sistema):
    assert tem_memoria(sistema) is False


# --- utilitário deslocar ---------------------------------------------------
def test_deslocar_atrasa_e_adianta():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    assert np.array_equal(deslocar(x, 1), [0.0, 1.0, 2.0, 3.0])
    assert np.array_equal(deslocar(x, -1), [2.0, 3.0, 4.0, 0.0])
    assert np.array_equal(deslocar(x, 0), x)
