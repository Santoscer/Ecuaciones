"""Modelo analítico de enfriamiento de Newton para una CPU."""
from __future__ import annotations
import math
from collections.abc import Iterable


def _finite(value: float, name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} debe ser un número.") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} debe ser finito.")
    return result


def temperatura(t: float | Iterable[float], T0: float, Ta: float, k: float):
    """Calcula T(t)=Ta+(T0-Ta)e^(-kt); tiempo en minutos y k en min⁻¹."""
    T0, Ta, k = _finite(T0, "T0"), _finite(Ta, "Ta"), _finite(k, "k")
    if k <= 0:
        raise ValueError("k debe ser positiva.")
    if isinstance(t, (int, float)):
        t = _finite(t, "t")
        if t < 0:
            raise ValueError("t no puede ser negativo.")
        return Ta + (T0 - Ta) * math.exp(-k * t)
    import numpy as np
    times = np.asarray(t, dtype=float)
    if not np.all(np.isfinite(times)) or np.any(times < 0):
        raise ValueError("Todos los tiempos deben ser finitos y no negativos.")
    return Ta + (T0 - Ta) * np.exp(-k * times)


def tiempo_objetivo(T0: float, Ta: float, T_obj: float, k: float) -> float | None:
    """Tiempo analítico en minutos; None si el objetivo es inalcanzable.

    Para enfriamiento (T0 > Ta), solo hay cruce si Ta < T_obj < T0.
    """
    T0, Ta, objetivo, k = (_finite(T0, "T0"), _finite(Ta, "Ta"),
                           _finite(T_obj, "T_obj"), _finite(k, "k"))
    if k <= 0:
        raise ValueError("k debe ser positiva.")
    if T0 <= Ta or not Ta < objetivo < T0:
        return None
    return math.log((T0 - Ta) / (objetivo - Ta)) / k


def convertir_tiempo(valor: float, unidad: str) -> float:
    """Convierte segundos u horas a minutos."""
    valor = _finite(valor, "valor")
    if valor < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    factores = {"segundos": 1 / 60, "minutos": 1.0, "horas": 60.0}
    if unidad not in factores:
        raise ValueError("Unidad inválida: use segundos, minutos u horas.")
    return valor * factores[unidad]


def solucion_simbolica():
    """Devuelve con SymPy la solución analítica general con condición inicial."""
    import sympy as sp
    t, T0, Ta, k = sp.symbols("t T_0 T_a k", real=True)
    T = sp.Function("T")
    expresion = Ta + (T0 - Ta) * sp.exp(-k * t)
    return sp.Eq(T(t), expresion)
