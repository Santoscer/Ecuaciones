"""Gráficas Plotly para los resultados de simulación."""
import plotly.express as px

def grafica_temperatura(curvas, T0, Ta, objetivo=None):
    larga = curvas.melt(id_vars="tiempo_min", var_name="Sistema", value_name="Temperatura (°C)")
    fig = px.line(larga, x="tiempo_min", y="Temperatura (°C)", color="Sistema",
                  title="Enfriamiento de la CPU", labels={"tiempo_min": "Tiempo (min)"})
    fig.add_hline(y=Ta, line_dash="dot", annotation_text=f"Ambiente: {Ta:g} °C")
    fig.add_hline(y=T0, line_dash="dot", line_color="gray", annotation_text=f"Inicial: {T0:g} °C")
    if objetivo is not None:
        fig.add_hline(y=objetivo, line_dash="dash", line_color="red", annotation_text=f"Objetivo: {objetivo:g} °C")
    fig.update_layout(hovermode="x unified", legend_title="Sistema", margin=dict(l=15,r=15,t=55,b=15))
    return fig
