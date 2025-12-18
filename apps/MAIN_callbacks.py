# ======================================================================
# MAIN_callbacks.py — AI4HyperTherm (compatível com layout real)
# ======================================================================

from dash import Input, Output, State, ctx, no_update
try:
    # Dash >= 2.9
    from dash import ctx
except Exception:
    # Compatibilidade com versões antigas
    from dash import callback_context as ctx

from dash.exceptions import PreventUpdate
from main import app
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time, random
import dash  # necessário para dash.no_update

########################################################################################################################
# Import Python Files
########################################################################################################################
from apps.MAIN_apps_list import *
from layouts.layouts_list import *
from surrogate_model.MLP_KerasPredict import *
from apps.HyperthermiaOptimization_Problem import run_hyperthermia_optimization


#######################################################################################################################
# Gera os TABS
#######################################################################################################################
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def update_tab_content(selected_tab):
    if selected_tab == 'TAB_Simulation':
        return layout_TAB_Simulation()
    elif selected_tab == 'TAB_Optimization':
        return layout_TAB_Optimization()
    elif selected_tab == 'TAB_Help':
        return layout_help()
    elif selected_tab == 'TAB_About':
        return layout_TAB_About()

#######################################################################################################################
# Callbacks – AI4HyperTherm (TAB_Config)
#######################################################################################################################

# ==========================================================
# 1) Sincronização Input ↔ Slider (bidirecional, sem ping-pong)
# ==========================================================

# mapeie os limites de cada par (use os mesmos do seu layout)
RANGES = {
    "input-vf":            (3.0, 5.0),
    "input-h":             (1500, 4000),
    "input-f":             (100000, 300000),
    "input-r":             (5.0, 10.0),
    "input-tumor-radius":  (5.0, 10.0),
    "input-eccentricity":  (0.0, 0.90),
}

def _coerce_and_clamp(x, lo, hi):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if v < lo: v = lo
    if v > hi: v = hi
    return v

def sync_pair(input_id, slider_id):
    @app.callback(
        [Output(input_id, "value"), Output(slider_id, "value")],
        [Input(input_id, "value"),   Input(slider_id, "value")],
        prevent_initial_call=True,
    )
    def _sync(v_input, v_slider):
        trg = ctx.triggered_id
        lo, hi = RANGES[input_id]

        # Usuário digitou no campo numérico
        if trg == input_id:
            v = _coerce_and_clamp(v_input, lo, hi)
            if v is None:
                return no_update, no_update   # valor inválido (ex.: campo vazio)
            return no_update, v              # atualiza o slider

        # Usuário moveu o slider
        if trg == slider_id:
            return v_slider, no_update       # reflete no input

        return no_update, no_update

# Pares
sync_pair("input-vf",            "slider-vf")
sync_pair("input-h",             "slider-h")
sync_pair("input-f",             "slider-f")
sync_pair("input-r",             "slider-r")
sync_pair("input-tumor-radius",  "slider-tumor-radius")
sync_pair("input-eccentricity",  "slider-eccentricity")


# ==========================================================
# 2) Elipse tumoral + predição única via MLP
# ==========================================================
@app.callback(
    [
        Output("out-tc", "children"),
        Output("out-stime", "children"),
        Output("out-tmin", "children"),
        Output("out-tavg", "children"),
        Output("out-tstd", "children"),
        Output("out-sar", "children"),
        Output("out-rafet", "children"),
        Output("ellipse-graph", "figure"),
    ],
    [
        Input("input-tumor-radius", "value"),
        Input("input-eccentricity", "value"),
        Input("input-vf", "value"),
        Input("input-h", "value"),
        Input("input-f", "value"),
        Input("input-r", "value"),
    ],
)
def update_ellipse(tumor_mm, e, vf, h, f, r_nm):
    if tumor_mm is None or e is None:
        return (
            dash.no_update, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update,
            dash.no_update, go.Figure()
        )

    a = tumor_mm
    b = a * np.sqrt(max(0.0, 1.0 - float(e)**2))     # menor eixo
    theta = np.linspace(0, 2*np.pi, 300)
    x, y = a*np.cos(theta), b*np.sin(theta)

    fig = go.Figure([
        go.Scatter(
            x=x, y=y, mode="lines",
            line=dict(color="#007BFF", width=3),
            fill="toself", fillcolor="rgba(0,123,255,0.15)",
            name="Tumor Geometry"
        )
    ])
    lim = (10.0) * 1.2
    fig.update_xaxes(
        range=[-lim, lim], scaleanchor="y", scaleratio=1,
        showgrid=False, zeroline=True, zerolinecolor="lightgray"
    )
    fig.update_yaxes(
        range=[-lim, lim], showgrid=False, scaleratio=1,
        zeroline=True, zerolinecolor="lightgray"
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=25, b=20),
        showlegend=False,
        title=dict(text=f"Elliptical Cross-section (a={a:.2f} mm, e={e:.2f})", x=0.5),
        xaxis_title="x (mm)", yaxis_title="y (mm)",
    )

    # Conversões de unidades
    vf_frac   = vf / 100.0
    r_m       = r_nm * 1e-9
    tumor_m   = tumor_mm * 1e-3

    input_data = np.array([[vf_frac, h, f, r_m, tumor_m, e]])
    output = PredictValues(input_data, Tensor=True)

    tc, st, tmin, tavg, tstd, sar, raf = output[0]
    raf_mm = raf * 1000.0

    fmt = lambda v, d=2: f"{v:.{d}f}"
    return (
        fmt(tc, 1),
        fmt(st, 1),
        fmt(tmin, 1),
        fmt(tavg, 1),
        fmt(tstd, 2),
        fmt(sar, 1),
        fmt(raf_mm, 1),
        fig
    )

####################################################################################################
# RUN OPTIMIZATION CALLBACK
####################################################################################################

@app.callback(
    Output("opt-results-table", "data"),
    Output("opt-pareto-graph", "figure"),
    Output("opt-status", "children"),
    Input("btn-run-optimization", "n_clicks"),
    State("opt-tumor-radius", "value"),
    State("opt-eccentricity", "value"),
    State("opt-vf", "value"),
    State("opt-rnm", "value"),
    State("opt-tc-max", "value"),
    State("opt-tavg-min", "value"),  # agora interpretado como TMIN mínima
    State("opt-pop-size", "value"),
    State("opt-n-gen", "value"),
    prevent_initial_call=True
)
def run_optimization_callback(
    n_clicks,
    tumor_mm,
    e,
    vf_pct,
    r_nm,
    tc_max,
    tmin_min,   # semântica: limiar mínimo da menor temperatura tumoral
    pop_size,
    n_gen
):
    try:
        # --- Status inicial ---
        status_msg = (
            f"Running optimization for tumor={tumor_mm:.1f} mm, "
            f"eccentricity={e:.2f}, vf={vf_pct:.1f}%, r={r_nm:.1f} nm, "
            f"TC_max={tc_max:.1f} °C, TMIN_min={tmin_min:.1f} °C..."
        )
        print(status_msg)

        # --- Executa otimização ---
        df, pareto = run_hyperthermia_optimization(
            tumor_mm=tumor_mm,
            e=e,
            vf_pct=vf_pct,
            r_nm=r_nm,
            tc_max=tc_max,
            tavg_min=tmin_min,  # aqui tavg_min é o limiar usado para TMIN dentro do problema
            pop_size=pop_size,
            n_gen=n_gen
        )

        if df.empty:
            return (
                no_update,
                no_update,
                "⚠️ No feasible solutions found. Try relaxing the thermal constraints "
                "(Maximum central temperature or minimum tumor temperature)."
            )

        # ============================================================
        # --- Cria o gráfico 3D interativo (Pareto Front) ---
        # ============================================================
        fig = px.scatter_3d(
            df,
            x="TSTD",
            y="S_TIME(s)",
            z="TAVG(°C)",
            color="TAVG(°C)",
            hover_data=[
                "vf(%)",
                "H(A/m)",
                "f(Hz)",
                "r_nm",
                "TMIN(°C)",   # agora explícito no hover
                "SAR(W/kg)",
                "RAF(mm)",
            ],
            color_continuous_scale="Viridis",
            title="Pareto Front – Treatment Efficiency vs Uniformity vs Safety"
        )

        fig.update_traces(marker=dict(size=6, opacity=0.8))
        fig.update_layout(
            scene=dict(
                xaxis_title="Temperature Uniformity (°C)",
                yaxis_title="Treatment Time (s)",
                zaxis_title="Average Tumor Temperature (°C)",
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            coloraxis_colorbar=dict(title="TAVG (°C)")
        )

        # ============================================================
        # --- Atualiza status final ---
        # ============================================================
        status_msg = (
            f"✅ Optimization completed successfully — {len(df)} feasible solutions found."
        )

        return df.to_dict("records"), fig, status_msg

    except Exception as e:
        print("❌ Optimization error:", str(e))
        return no_update, no_update, f"❌ Error during optimization: {e}"
