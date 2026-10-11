# Modelo matemático

## Ley de enfriamiento de Newton

Se supone que la rapidez de variación térmica es proporcional a la diferencia entre la CPU y el ambiente: `dT/dt = -k(T-Ta)`, donde `k>0`. Separando variables e integrando: `ln|T-Ta|=-kt+C`. Con `T(0)=T0` se obtiene `T(t)=Ta+(T0-Ta)e^(-kt)`.

Para `T0>Ta`, el objetivo se alcanza solo cuando `Ta<T_obj<T0`. El tiempo es `t=ln((T0-Ta)/(T_obj-Ta))/k`. Si está por debajo o en `Ta`, no hay cruce finito; si está por encima de `T0`, no es objetivo de enfriamiento.

## Unidades y supuestos

El programa usa minutos, grados Celsius y `k` en min⁻¹. Si se convierte el eje temporal, debe convertirse también k de forma coherente. Ambiente y k constantes; sin carga térmica adicional. Las cuatro k incluidas son valores hipotéticos para demostrar tendencias, no mediciones de productos.
