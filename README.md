# Simulación matemática del proceso de enfriamiento de un computador aplicando la Ley de Enfriamiento de Newton

Proyecto universitario para Ecuaciones Diferenciales de Ingeniería de Sistemas.

## Descripción y pregunta problema

¿Cómo cambia la evolución de temperatura de una CPU al comparar distintas constantes ilustrativas de refrigeración, manteniendo iguales las condiciones iniciales y ambientales?

## Objetivo

Implementar y visualizar la solución analítica de la Ley de Enfriamiento de Newton, estimar cruces de una temperatura objetivo y comparar cuatro escenarios editables.

## Funcionalidades

- Simulación interactiva de temperatura y gráfica Plotly.
- Comparación común de disipación pasiva, aire con ventilador, refrigeración líquida y aire de alto rendimiento.
- Indicador del primer sistema que cruza el objetivo dentro del tiempo simulado.
- Desarrollo por separación de variables y análisis de supuestos.
- Descarga CSV y reporte PDF opcional.

Las k iniciales (0.025, 0.055, 0.080 y 0.100 min⁻¹) son hipotéticas, editables y no representan especificaciones reales.

## Fundamento matemático

`dT/dt=-k(T-Ta)` y `T(t)=Ta+(T0-Ta)e^(-kt)`. Para un objetivo alcanzable `Ta<T_obj<T0`: `t_obj=ln((T0-Ta)/(T_obj-Ta))/k`. Unidades: °C, minutos y min⁻¹. El modelo considera Ta y k constantes y no representa carga térmica activa. Detalles en [docs/modelo_matematico.md](docs/modelo_matematico.md).

## Tecnologías y módulos

Python 3.11, Streamlit, NumPy, Pandas, Plotly, SymPy (disponible como dependencia para extensiones simbólicas), pytest y ReportLab.

- `app.py`: aplicación y navegación.
- `modelo.py`: solución y validación matemática.
- `simulacion.py`: curvas y resumen comparativo.
- `graficas.py`: figura Plotly.
- `exportacion.py`: CSV e informe PDF.
- `tests/`: verificaciones automatizadas del modelo y la comparación de escenarios.

## Requisitos y ejecución en Windows PowerShell

Se recomienda Python 3.11. Verifica versiones instaladas con `py --list-paths` (o `py -0p`); si no aparece 3.11, instala una versión compatible y sustituye `-3.11` en el comando de creación.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest -v
python -m streamlit run app.py
```

Si PowerShell bloquea la activación, ejecuta directamente:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit imprime la dirección local, normalmente `http://localhost:8501`.

## Interfaz del laboratorio

La interfaz ofrece un panel lateral para configurar temperaturas, objetivo, tiempo, sistemas y coeficientes `k`. La navegación principal divide el trabajo en cuatro vistas: simulación, comparación, explicación matemática y descargas. El tema usa una paleta clara en tonos verde azulado, tarjetas con bordes y controles nativos adaptables a pantallas pequeñas.

## Ejemplo de uso

En la barra lateral conserva T₀=85 °C y Ta=24 °C, selecciona los cuatro sistemas y fija un objetivo entre Ta y T₀. La tabla informa el tiempo analítico y si cruza antes del fin de la ventana. Ajusta una k para observar cómo cambia la pendiente.

## Git y GitHub

El `.gitignore` excluye entornos, cachés y secretos. Para revisar cambios: `git status`, `git diff`. Para commits pequeños: `git add <archivos>`, `git diff --cached`, `git commit -m "feat: ..."`.

Para GitHub, crea un repositorio vacío, copia su URL real y conéctala: `git remote add origin <URL_REAL_DEL_REPOSITORIO>`. Luego revisa rama y remoto antes de sincronizar; si corresponde: `git push -u origin main`. Nunca incluyas tokens en el proyecto ni fuerces un push para reemplazar historial remoto.

## Limitaciones

El modelo supone una CPU térmicamente uniforme, ambiente constante, k constante y ausencia de generación de calor adicional. Un computador real puede tener cargas variables, múltiples componentes, control de ventiladores, resistencia térmica no lineal y temperaturas de ambiente cambiantes. Los valores de refrigeración son ilustrativos y requieren calibración experimental para predicción de hardware.
