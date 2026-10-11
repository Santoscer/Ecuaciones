import math
import numpy as np
import pytest
from modelo import temperatura, tiempo_objetivo, convertir_tiempo

def test_temperatura_inicial():
    assert temperatura(0, 80, 20, .1) == 80

def test_solucion_analitica():
    assert temperatura(10, 80, 20, .1) == pytest.approx(20 + 60 * math.exp(-1))

def test_k_mayor_enfria_mas_rapido():
    assert temperatura(5, 80, 20, .2) < temperatura(5, 80, 20, .1)

def test_se_aproxima_a_ambiente():
    assert temperatura(1000, 80, 20, .1) == pytest.approx(20)

def test_entradas_invalidas():
    for args in [(0,80,20,0), (-1,80,20,.1), (float('nan'),80,20,.1)]:
        with pytest.raises(ValueError): temperatura(*args)

def test_tiempo_objetivo():
    assert tiempo_objetivo(80, 20, 50, .1) == pytest.approx(math.log(2)/.1)

def test_objetivo_inalcanzable():
    assert tiempo_objetivo(80, 20, 20, .1) is None
    assert tiempo_objetivo(80, 20, 90, .1) is None

def test_conversion_tiempo():
    assert convertir_tiempo(120, 'segundos') == 2
    assert convertir_tiempo(2, 'horas') == 120
    with pytest.raises(ValueError): convertir_tiempo(1, 'días')
