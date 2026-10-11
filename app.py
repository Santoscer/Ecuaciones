"""Dashboard Streamlit del simulador de enfriamiento de CPU."""
import streamlit as st
import sympy as sp
from simulacion import ESCENARIOS, comparar_escenarios
from modelo import solucion_simbolica
from graficas import grafica_temperatura
from exportacion import csv_bytes, pdf_bytes

st.set_page_config(page_title="Enfriamiento de CPU", page_icon="❄️", layout="wide")
st.markdown("""<style>
.block-container{max-width:1400px;padding-top:2rem} [data-testid="stMetric"]{background:#f3f7fb;padding:1rem;border-radius:12px}
.hero{padding:1.5rem 1.8rem;border-radius:18px;background:linear-gradient(120deg,#102a43,#1976a5);color:white;margin-bottom:1rem}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>❄️ Simulador de enfriamiento de CPU</h1><p>Explora la Ley de Enfriamiento de Newton y compara estrategias térmicas.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Condiciones")
    T0 = st.number_input("Temperatura inicial (°C)", 30.0, 120.0, 85.0, 1.0)
    Ta = st.number_input("Temperatura ambiente (°C)", -10.0, 50.0, 24.0, 1.0)
    objetivo = st.number_input("Temperatura objetivo (°C)", -10.0, 120.0, 40.0, 1.0)
    duracion = st.slider("Duración de simulación (min)", 5, 240, 60)
    pasos = st.slider("Resolución (puntos)", 50, 1000, 300, 50)
    st.caption("k hipotéticas, editables en min⁻¹. Modelo ilustrativo, no representa un producto específico.")
    seleccion = st.multiselect("Sistemas a comparar", list(ESCENARIOS), default=list(ESCENARIOS))
    constantes = {}
    for name in seleccion:
        constantes[name] = st.number_input(f"k · {name} (min⁻¹)", min_value=0.001, max_value=1.0,
                                           value=ESCENARIOS[name], step=0.005, format="%.3f", key=f"k_{name}")

if T0 <= Ta:
    st.warning("Para estudiar enfriamiento, la temperatura inicial debe superar la ambiente.")
if not constantes:
    st.info("Selecciona al menos un sistema en el panel lateral.")
else:
    curvas, resumen = comparar_escenarios(T0, Ta, float(duracion), pasos, constantes, objetivo)
    cruces = [(row["Sistema"], row["Tiempo objetivo (min)"]) for _, row in resumen.iterrows()
              if row["Alcanza objetivo en intervalo"]]
    cols = st.columns(3)
    cols[0].metric("Sistemas comparados", len(constantes))
    cols[1].metric("Temperatura inicial", f"{T0:.1f} °C")
    ganador = min(cruces, key=lambda par: par[1]) if cruces else None
    cols[2].metric("Primero al objetivo", ganador[0] if ganador else "No cruza en el intervalo",
                   f"{ganador[1]:.1f} min" if ganador else None)
    tab_sim, tab_compare, tab_math, tab_exp, tab_results, tab_about = st.tabs([
        "Simulador", "Comparación", "Modelo matemático", "Experimentación", "Resultados y exportación", "Proyecto"])
    with tab_sim:
        st.subheader("Evolución térmica")
        st.plotly_chart(grafica_temperatura(curvas, T0, Ta, objetivo), use_container_width=True)
        st.caption("La asíntota es la temperatura ambiente; el modelo ideal no la alcanza en tiempo finito.")
    with tab_compare:
        st.subheader("Comparación de sistemas")
        st.dataframe(resumen, hide_index=True, use_container_width=True)
        if ganador:
            st.success(f"{ganador[0]} llega primero a {objetivo:g} °C, en {ganador[1]:.2f} min.")
        else:
            st.info("Ningún escenario cruza el objetivo dentro del intervalo simulado (o el objetivo no es alcanzable).")
    with tab_math:
        st.subheader("Separación de variables")
        st.latex(r"\frac{dT}{dt}=-k(T-T_a),\quad \frac{dT}{T-T_a}=-k\,dt")
        st.latex(r"\ln|T-T_a|=-kt+C")
        st.latex(sp.latex(solucion_simbolica()))
        st.markdown("La diferencia entre CPU y ambiente decae exponencialmente. `k` mide rapidez: a mayor `k`, menor tiempo para acercarse a `Tₐ`. Se usan minutos y °C; `k` se expresa en min⁻¹.")
        st.latex(r"t_{obj}=\frac{1}{k}\ln\left(\frac{T_0-T_a}{T_{obj}-T_a}\right),\quad T_a<T_{obj}<T_0")
        st.info("Hipótesis: ambiente constante, `k` constante, capacidad térmica uniforme y ausencia de generación de calor una vez inicia el enfriamiento.")
    with tab_exp:
        st.subheader("Experimenta")
        st.write("Cambia T₀, Tₐ, el objetivo, la duración y cada constante k en la barra lateral; las condiciones iniciales son comunes a todos los sistemas.")
        if cruces:
            st.write("Orden de llegada en la ventana actual:")
            for name, time in sorted(cruces, key=lambda pair: pair[1]):
                st.write(f"• **{name}** — {time:.2f} min")
    with tab_results:
        st.subheader("Análisis de resultados")
        st.dataframe(resumen, hide_index=True, use_container_width=True)
        st.download_button("Descargar datos de temperatura (CSV)", csv_bytes(curvas), "enfriamiento_cpu.csv", "text/csv")
        pdf = pdf_bytes(curvas, resumen, T0, Ta)
        st.download_button("Descargar informe (PDF)", pdf, "informe_enfriamiento_cpu.pdf", "application/pdf")
        st.caption("El CSV contiene la serie temporal de todos los sistemas seleccionados.")
    with tab_about:
        st.subheader("Proyecto universitario")
        st.markdown("""**Asignatura:** Ecuaciones Diferenciales de Ingeniería de Sistemas

**Pregunta problema:** ¿Cómo cambia la rapidez de enfriamiento de una CPU al variar el sistema de refrigeración?

**Objetivo:** simular la solución analítica de Newton y comparar escenarios con condiciones idénticas.""")
        st.markdown("Los coeficientes de los cuatro sistemas son valores hipotéticos y editables. La simulación no sustituye mediciones de hardware: la carga, la temperatura ambiente y el control del ventilador pueden cambiar en sistemas reales.")
