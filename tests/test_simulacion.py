import pytest
from simulacion import comparar_escenarios

def test_condiciones_comunes_y_tiempo_de_cruce():
    curvas, resumen = comparar_escenarios(80, 20, 30, 101, {"lento": .05, "rápido": .1}, 40)
    assert curvas["lento"].iloc[0] == curvas["rápido"].iloc[0] == 80
    assert curvas["tiempo_min"].iloc[-1] == 30
    tiempos = resumen.set_index("Sistema")["Tiempo objetivo (min)"]
    assert tiempos["rápido"] < tiempos["lento"]

def test_parametros_invalidos():
    with pytest.raises(ValueError): comparar_escenarios(80,20,10,1,{"x":.1})
    with pytest.raises(ValueError): comparar_escenarios(80,20,10,10,{})
