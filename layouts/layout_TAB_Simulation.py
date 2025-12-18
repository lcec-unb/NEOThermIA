# ======================================================================
# AI4HyperTherm — Magnetic Hyperthermia Predictor
# LAYOUT (UI) — tema claro, sliders limpos, unidades em nm/mm
# ======================================================================

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html


def layout_TAB_Simulation():
    # ------------------------------------------------------------
    # Helper: campo numérico + slider (mesma largura, sem marks)
    # ------------------------------------------------------------
    def numeric_with_slider(label, input_id, slider_id,
                            min_val, max_val, step, value, unit, help_text=None):
        return html.Div([
            dbc.Label(label, className="fw-semibold mt-2"),
            dbc.Input(
                id=input_id, type="number", value=value, step=step,
                min=min_val, max=max_val, debounce=True, style={"marginBottom": "6px"}
            ),
            dcc.Slider(
                id=slider_id,
                min=min_val, max=max_val, step=step, value=value,
                marks=None,
                included=False,
                updatemode="drag",
                tooltip={"always_visible": False},
                className="mb-1"
            ),
            dbc.FormText(help_text or f"Range: {min_val:g} – {max_val:g} {unit}")
        ], className="mb-3")

    # ------------------------------------------------------------
    # Inputs (com sliders e unidades amigáveis)
    # ------------------------------------------------------------
    inputs_card = dbc.Card([
        dbc.CardHeader("Input Parameters", className="bg-light fw-bold text-dark"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    numeric_with_slider(
                        "Volume Fraction (%)", "input-vf", "slider-vf",
                        3.0, 5.0, 0.01, 4.0, "%"
                    ),
                ], md=4),
                dbc.Col([
                    numeric_with_slider(
                        "Magnetic Field Intensity (A/m)", "input-h", "slider-h",
                        1500, 4000, 1, 2000, "A/m"
                    ),
                ], md=4),
                dbc.Col([
                    numeric_with_slider(
                        "Field Frequency (Hz)", "input-f", "slider-f",
                        100000, 300000, 100, 150000, "Hz"
                    ),
                ], md=4),
            ], className="gy-2"),

            dbc.Row([
                dbc.Col([
                    numeric_with_slider(
                        "Nanoparticle Radius (nm)", "input-r", "slider-r",
                        5.0, 10.0, 0.1, 6.0, "nm",
                    ),
                ], md=4),
                dbc.Col([
                    numeric_with_slider(
                        "Tumor Radius (mm)", "input-tumor-radius", "slider-tumor-radius",
                        5.0, 10.0, 0.1, 7.0, "mm",
                    ),
                ], md=4),
                dbc.Col([
                    numeric_with_slider(
                        "Eccentricity (0–0.90)", "input-eccentricity", "slider-eccentricity",
                        0.0, 0.90, 0.01, 0.70, "–",
                        "0 = circle; → 1 = more elliptical"
                    ),
                ], md=4),
            ], className="gy-2"),
        ])
    ], className="mb-4 shadow-sm")

    # ------------------------------------------------------------
    # Visualização da elipse (conforme Tumor Radius & Eccentricity)
    # ------------------------------------------------------------
    ellipse_card = dbc.Card([
        dbc.CardHeader("Tumor Geometry Visualization", className="bg-light fw-bold text-dark"),
        dbc.CardBody([
            html.P(
                "The ellipse below represents the tumor cross-section based on Tumor Radius (mm) and Eccentricity.",
                className="text-secondary"
            ),
            dcc.Graph(
                id="ellipse-graph",
                style={"height": "360px"},
                config={"displayModeBar": False}
            )
        ])
    ], className="mb-4 shadow-sm")

    # ------------------------------------------------------------
    # Outputs (métricas previstas)
    # ------------------------------------------------------------
    outputs_card = dbc.Card([
        dbc.CardHeader("Predicted Results", className="bg-light fw-bold text-dark"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(html.Div([
                    html.H6("TC (°C)", className="text-muted mb-1"),
                    html.H4(id="out-tc", children="—", className="fw-bold text-primary")
                ]), md=2),
                dbc.Col(html.Div([
                    html.H6("TIME (s)", className="text-muted mb-1"),
                    html.H4(id="out-stime", children="—", className="fw-bold text-primary")
                ]), md=2),
                dbc.Col(html.Div([
                    html.H6("TMIN (°C)", className="text-muted mb-1"),
                    html.H4(id="out-tmin", children="—", className="fw-bold text-primary")
                ]), md=2),
                dbc.Col(html.Div([
                    html.H6("TAVG (°C)", className="text-muted mb-1"),
                    html.H4(id="out-tavg", children="—", className="fw-bold text-primary")
                ]), md=2),
                dbc.Col(html.Div([
                    html.H6("TSTD (°C)", className="text-muted mb-1"),
                    html.H4(id="out-tstd", children="—", className="fw-bold text-primary")
                ]), md=2),
            ], className="gy-3"),
            dbc.Row([
                dbc.Col(html.Div([
                    html.H6("SAR (W/kg)", className="text-muted mb-1"),
                    html.H4(id="out-sar", children="—", className="fw-bold text-success")
                ]), md=2),
                dbc.Col(html.Div([
                    html.H6("Affected radius (mm)", className="text-muted mb-1"),
                    html.H4(id="out-rafet", children="—", className="fw-bold text-success")
                ]), md=3),
            ], className="gy-2 mt-1"),
        ])
    ], className="shadow-sm")

    # ------------------------------------------------------------
    # Layout principal — gráfico (esq) / ações+resultados (dir)
    # ------------------------------------------------------------
    layout = html.Div([
        dbc.Container([
            inputs_card,

            dbc.Row([
                # Coluna esquerda: gráfico
                dbc.Col(ellipse_card, md=6),

                # Coluna direita:  resultados
                dbc.Col([
                    outputs_card
                ], md=6),
            ], className="g-4 mb-4"),

        ], fluid=True, className="p-4 bg-white text-dark")
    ])

    return layout
