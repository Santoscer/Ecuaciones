"""Interfaz del laboratorio interactivo de enfriamiento de CPU."""
import streamlit as st
import sympy as sp

from exportacion import csv_bytes, pdf_bytes
from graficas import grafica_temperatura
from modelo import solucion_simbolica
from simulacion import ESCENARIOS, comparar_escenarios

# La configuración va primero para evitar parpadeos al cargar la página.
st.set_page_config(
    page_title="Laboratorio térmico | CPU",
    page_icon=":material/device_thermostat:",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVEGACION = ["Simular", "Comparar", "Entender el modelo", "Descargar"]

# Panel único de controles: todas las comparaciones heredan las mismas condiciones.
with st.sidebar:
    st.header("Tu experimento", icon=":material/tune:")
    st.caption("Ajusta las condiciones y explora cómo cambia el enfriamiento.")

    T0 = st.number_input(
        "Temperatura inicial de la CPU (°C)",
        min_value=25.0,
        max_value=120.0,
        value=85.0,
        step=1.0,
        help="Temperatura de la CPU justo al comenzar la simulación.",
    )
    Ta = st.number_input(
        "Temperatura ambiente (°C)",
        min_value=-10.0,
        max_value=60.0,
        value=24.0,
        step=1.0,
        help="Se considera constante durante todo el experimento.",
    )
    objetivo = st.number_input(
        "Temperatura objetivo (°C)",
        min_value=-10.0,
        max_value=120.0,
        value=40.0,
        step=1.0,
        help="El simulador indica qué sistema llega primero, si el objetivo es alcanzable.",
    )
    duracion = st.slider("Tiempo de observación (minutos)", 5, 240, 60, 5)

    sistemas = st.pills(
        "Sistemas de refrigeración",
        options=list(ESCENARIOS),
        selection_mode="multi",
        default=list(ESCENARIOS),
        help="Compara uno o varios sistemas. Todos parten de las mismas temperaturas.",
        width="stretch",
    ) or []

    # Los coeficientes iniciales son didácticos; el usuario puede modificarlos aquí.
    constantes = {}
    if sistemas:
        with st.expander("Ajustar rapidez de cada sistema", icon=":material/speed:"):
            for nombre in sistemas:
                constantes[nombre] = st.number_input(
                    f"k · {nombre} (min⁻¹)",
                    min_value=0.001,
                    max_value=1.0,
                    value=ESCENARIOS[nombre],
                    step=0.005,
                    format="%.3f",
                    key=f"k_{nombre}",
                    help="Una k mayor representa un enfriamiento más rápido en este modelo.",
                )

    with st.expander("Resolución de la gráfica", icon=":material/tune:"):
        pasos = st.slider("Puntos de cálculo", 50, 1000, 300, 50)
        st.caption("Más puntos producen una curva más detallada.")

    st.caption("Los valores de k son hipotéticos y editables; no son especificaciones de hardware.")

# Encabezado y navegación principal para que cada tarea tenga una ruta clara.
st.title("Laboratorio de enfriamiento", icon=":material/device_thermostat:")
st.markdown(
    "Explora la **Ley de Enfriamiento de Newton** y descubre cómo la rapidez de refrigeración "
    "cambia la temperatura de una CPU."
)
st.badge("MODELO MATEMÁTICO INTERACTIVO", icon=":material/science:", color="blue")
st.badge("Tiempo en minutos · temperatura en °C", icon=":material/schedule:", color="green")

vista = st.segmented_control(
    "Secciones del laboratorio",
    options=NAVEGACION,
    default="Simular",
    label_visibility="collapsed",
    width="stretch",
)

if not constantes:
    st.info("Selecciona al menos un sistema en el panel lateral para comenzar.", icon=":material/touch_app:")
else:
    # El mismo conjunto de curvas alimenta el gráfico, la tabla y las descargas.
    curvas, resumen = comparar_escenarios(
        T0, Ta, float(duracion), pasos, constantes, objetivo
    )
    cruces = [
        (fila["Sistema"], fila["Tiempo objetivo (min)"])
        for _, fila in resumen.iterrows()
        if fila["Alcanza objetivo en intervalo"]
    ]
    ganador = min(cruces, key=lambda elemento: elemento[1]) if cruces else None

    if T0 <= Ta:
        st.warning(
            "Para observar un proceso de enfriamiento, la temperatura inicial debe superar "
            "la temperatura ambiente.",
            icon=":material/warning:",
        )

    if vista == "Simular":
        st.subheader("Tu simulación")
        if ganador:
            mensaje_tiempo = f"{ganador[1]:.1f} min"
        else:
            mensaje_tiempo = "Sin cruce"

        # Indicadores breves resumen el estado antes de mostrar la gráfica.
        with st.container(horizontal=True, gap="medium"):
            st.metric("Temperatura inicial", f"{T0:.1f} °C", border=True)
            st.metric("Temperatura ambiente", f"{Ta:.1f} °C", border=True)
            st.metric(
                "Primero al objetivo",
                ganador[0] if ganador else "Sin cruce",
                delta=mensaje_tiempo if ganador else "En esta ventana",
                delta_color="off",
                border=True,
            )

        with st.container(border=True):
            st.subheader("Así se enfría la CPU", icon=":material/show_chart:")
            st.caption(
                "Pasa el cursor sobre una curva para consultar la temperatura. "
                "La línea punteada marca el objetivo y la ambiente."
            )
            st.plotly_chart(
                grafica_temperatura(curvas, T0, Ta, objetivo),
                width="stretch",
                theme="streamlit",
                alt="Temperatura de la CPU frente al tiempo para cada sistema de refrigeración.",
            )

        if ganador:
            st.success(
                f"**{ganador[0]}** llega primero a {objetivo:g} °C, "
                f"en aproximadamente **{ganador[1]:.2f} minutos**.",
                icon=":material/check_circle:",
            )
        else:
            st.info(
                "Ningún sistema cruza el objetivo dentro del tiempo elegido, "
                "o la temperatura objetivo no es alcanzable según el modelo.",
                icon=":material/info:",
            )

        with st.expander("¿Cómo interpretar esta gráfica?", icon=":material/lightbulb:"):
            st.markdown(
                "Cada curva representa un sistema. Una curva que desciende más rápido "
                "corresponde a un valor de **k** mayor. La temperatura se aproxima a la "
                "del ambiente sin alcanzarla en tiempo finito en este modelo ideal."
            )

    elif vista == "Comparar":
        st.subheader("Comparación de sistemas")
        st.caption(
            "Las condiciones iniciales y la temperatura ambiente son iguales en todos los casos."
        )
        if ganador:
            st.success(
                f"El primero en alcanzar el objetivo es **{ganador[0]}** "
                f"({ganador[1]:.2f} min).",
                icon=":material/emoji_events:",
            )
        else:
            st.info("No hay cruces del objetivo en la ventana actual.", icon=":material/info:")

        with st.container(border=True):
            st.dataframe(
                resumen,
                hide_index=True,
                width="stretch",
                alt="Tabla comparativa de constantes, temperaturas finales y tiempos objetivo.",
            )

        sistemas_con_cruce = resumen[resumen["Alcanza objetivo en intervalo"]]
        if not sistemas_con_cruce.empty:
            st.subheader("¿Quién llega antes?", icon=":material/timer:")
            st.bar_chart(
                sistemas_con_cruce.set_index("Sistema")[["Tiempo objetivo (min)"]],
                horizontal=True,
                color="#137C78",
                x_label="Minutos para alcanzar el objetivo",
                y_label="Sistema",
                alt="Tiempo que tarda cada sistema en alcanzar la temperatura objetivo.",
            )

    elif vista == "Entender el modelo":
        st.subheader("La matemática detrás del enfriamiento")
        st.markdown(
            "La Ley de Newton supone que la CPU pierde calor a una rapidez proporcional "
            "a la diferencia entre su temperatura y la del ambiente."
        )
        with st.container(border=True):
            st.latex(r"\frac{dT}{dt}=-k(T-T_a)")
            st.caption("La rapidez de cambio depende de la diferencia térmica.")

        pasos_modelo = st.columns(3)
        pasos_modelo[0].markdown("**1 · Separar**")
        pasos_modelo[0].latex(r"\frac{dT}{T-T_a}=-k\,dt")
        pasos_modelo[1].markdown("**2 · Integrar**")
        pasos_modelo[1].latex(r"\ln|T-T_a|=-kt+C")
        pasos_modelo[2].markdown("**3 · Aplicar T(0)=T₀**")
        pasos_modelo[2].latex(sp.latex(solucion_simbolica()))

        st.markdown("**Tiempo para alcanzar una temperatura objetivo**")
        st.latex(
            r"t_{obj}=\frac{1}{k}\ln\left(\frac{T_0-T_a}{T_{obj}-T_a}\right),"
            r"\qquad T_a<T_{obj}<T_0"
        )
        with st.container(border=True):
            st.markdown("**Qué significa cada parámetro**")
            st.markdown(
                "- **T₀:** temperatura inicial de la CPU.\n"
                "- **Tₐ:** temperatura ambiente constante.\n"
                "- **k:** constante positiva de enfriamiento, en min⁻¹.\n"
                "- **t:** tiempo transcurrido, en minutos."
            )
        st.caption(
            "Supuestos: temperatura ambiente y k constantes, CPU uniforme y sin generación "
            "adicional de calor. Los coeficientes son valores ilustrativos, no mediciones reales."
        )

    elif vista == "Descargar":
        st.subheader("Resultados y exportación")
        st.caption("Guarda la serie temporal o un resumen del experimento en tu equipo.")
        with st.container(border=True):
            st.subheader("Resumen de la comparación", icon=":material/table_chart:")
            st.dataframe(
                resumen,
                hide_index=True,
                width="stretch",
                alt="Resumen de resultados del experimento de enfriamiento.",
            )

        # Las descargas se preparan solo en esta sección para mantener ligera la vista principal.
        with st.container(horizontal=True, gap="medium"):
            st.download_button(
                "Descargar datos CSV",
                data=csv_bytes(curvas),
                file_name="enfriamiento_cpu.csv",
                mime="text/csv",
                type="primary",
                icon=":material/download:",
            )
            st.download_button(
                "Descargar informe PDF",
                data=pdf_bytes(curvas, resumen, T0, Ta),
                file_name="informe_enfriamiento_cpu.pdf",
                mime="application/pdf",
                icon=":material/description:",
            )

with st.expander("Sobre este proyecto", icon=":material/school:"):
    st.markdown(
        "**Ecuaciones Diferenciales · Ingeniería de Sistemas**\n\n"
        "Proyecto académico para experimentar con la Ley de Enfriamiento de Newton. "
        "El modelo es didáctico: una CPU real puede tener carga variable, varios componentes "
        "y controles de ventilación que cambian con el tiempo."
    )
