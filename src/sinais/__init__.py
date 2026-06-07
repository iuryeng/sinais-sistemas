# -*- coding: utf-8 -*-
"""Pacote ``sinais`` — utilidades reutilizáveis dos notebooks de Sinais e Sistemas.

Submódulos:
- :mod:`sinais.sistemas` — classificação de sistemas em tempo discreto.
- :mod:`sinais.amostragem` — amostragem, aliasing e reconstrução.
"""
from .sistemas import (
    deslocar,
    eh_linear,
    eh_invariante_no_tempo,
    eh_causal,
    tem_memoria,
)
from .amostragem import (
    frequencia_nyquist,
    satisfaz_nyquist,
    freq_aparente,
    reconstrucao_sinc,
)

__all__ = [
    "deslocar",
    "eh_linear",
    "eh_invariante_no_tempo",
    "eh_causal",
    "tem_memoria",
    "frequencia_nyquist",
    "satisfaz_nyquist",
    "freq_aparente",
    "reconstrucao_sinc",
]
