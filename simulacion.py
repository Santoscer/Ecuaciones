"""Generación y comparación de escenarios de refrigeración."""
from __future__ import annotations
import pandas as pd
import numpy as np
from modelo import temperatura, tiempo_objetivo

ESCENARIOS = {
    "Disipación pasiva": 0.025,
    "Aire con ventilador": 0.055,
    "Refrigeración líquida": 0.080,
    "Aire de alto rendimiento": 0.100,
}

def comparar_escenarios(T0: float, Ta: float, duracion: float, pasos: int,
                        constantes: dict[str, float], objetivo: float | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Retorna curvas y resumen; todas comparten T0/Ta y la cuadrícula temporal."""
    if not isinstance(pasos, int) or pasos < 2:
        raise ValueError("Se requieren al menos 2 pasos enteros.")
    if not np.isfinite(duracion) or duracion <= 0:
        raise ValueError("La duración debe ser positiva y finita.")
    if not constantes:
        raise ValueError("Debe seleccionarse al menos un escenario.")
    tiempos = np.linspace(0.0, float(duracion), pasos)
    curvas = {"tiempo_min": tiempos}
    resumen = []
    for nombre, k in constantes.items():
        curvas[nombre] = temperatura(tiempos, T0, Ta, k)
        cruce = tiempo_objetivo(T0, Ta, objetivo, k) if objetivo is not None else None
        resumen.append({"Sistema": nombre, "k (min⁻¹)": k,
                        "Temperatura final (°C)": float(curvas[nombre][-1]),
                        "Tiempo objetivo (min)": cruce,
                        "Alcanza objetivo en intervalo": cruce is not None and cruce <= duracion})
    return pd.DataFrame(curvas), pd.DataFrame(resumen)
