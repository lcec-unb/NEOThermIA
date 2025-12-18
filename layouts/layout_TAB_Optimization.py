# ======================================================================
# AI4HyperTherm — Optimization Dashboard (Spinner abaixo do botão)
# ======================================================================

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table


def layout_TAB_Optimization():
    # ===============================================================
    # --- Patient Geometry ---
    # ===============================================================
    patient_card = dbc.Card([
        dbc.CardHeader("Patient Geometry", className="bg-light fw-bold text-dark"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Tumor Radius (mm)", className="fw-semibold"),
                    dcc.Slider(
                        id="opt-tumor-radius", min=3, max=15, step=0.1, value=7.0,
                        marks=None, tooltip={"always_visible": True, "placement": "bottom"},
                    ),
                ], md=6),
                dbc.Col([
                    dbc.Label("Eccentricity (0–0.90)", className="fw-semibold"),
                    dcc.Slider(
                        id="opt-eccentricity", min=0, max=0.9, step=0.01, value=0.7,
                        marks=None, tooltip={"always_visible": True, "placement": "bottom"},
                    ),
                ], md=6),
            ], className="gy-2 mt-2"),
            dbc.Alert(
                "These parameters describe the patient's tumor geometry used in the optimization.",
                color="secondary", className="mt-3 mb-0 small text-center"
            ),
        ])
    ], className="shadow-sm mb-4")

    # ===============================================================
    # --- Nanoparticle Properties ---
    # ===============================================================
    nanoparticle_card = dbc.Card([
        dbc.CardHeader("Magnetic Nanoparticle Properties", className="bg-light fw-bold text-dark"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Volume Fraction (%)", className="fw-semibold"),
                    dcc.Slider(
                        id="opt-vf", min=3.0, max=5.0, step=0.1, value=4.0,
                        marks=None, tooltip={"always_visible": True, "placement": "bottom"},
                    ),
                ], md=6),
                dbc.Col([
                    dbc.Label("Particle Radius (nm)", className="fw-semibold"),
                    dcc.Slider(
                        id="opt-rnm", min=5.0, max=10.0, step=0.1, value=8.0,
                        marks=None, tooltip={"always_visible": True, "placement": "bottom"},
                    ),
                ], md=6),
            ], className="gy-2 mt-2"),
            dbc.Alert(
                "These properties define the concentration and size of magnetic nanoparticles used for tumor heating.",
                color="secondary", className="mt-3 mb-0 small text-center"
            ),
        ])
    ], className="shadow-sm mb-4")

    # ===============================================================
    # --- Clinical Constraints ---
    # ===============================================================
    constraints_card = dbc.Card([
        dbc.CardHeader("Clinical Constraints", className="bg-light fw-bold text-dark"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Maximum Central Temperature (°C)", className="fw-semibold"),
                    dbc.Input(id="opt-tc-max", type="number", value=46.5, step=0.1, min=40, max=50)
                ], md=6),
                dbc.Col([
                    dbc.Label("Minimum Tumor Temperature (°C)", className="fw-semibold"),
                    # mantém id opt-tavg-min para compatibilidade com callback,
                    # mas semanticamente é o limiar mínimo de TMIN
                    dbc.Input(id="opt-tavg-min", type="number", value=42.0, step=0.1, min=35, max=45)
                ], md=6),
            ], className="gy-2"),
            dbc.Alert(
                "Defines the therapeutic range by limiting the maximum central temperature "
                "and enforcing a minimum temperature in the coldest tumor region.",
                color="info", className="mt-3 mb-0 small text-center"
            ),
        ])
    ], className="shadow-sm mb-3 h-100")

    # ===============================================================
    # --- Optimization Parameters ---
    # ===============================================================
    optimization_card = dbc.Card([
        dbc.CardHeader("Optimization Parameters", className="bg-light fw-bold text-dark"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Population Size", className="fw-semibold mt-2"),
                    dbc.Input(id="opt-pop-size", type="number", value=80, step=10, min=10, max=300)
                ], md=6),
                dbc.Col([
                    dbc.Label("Generations", className="fw-semibold mt-2"),
                    dbc.Input(id="opt-n-gen", type="number", value=100, step=10, min=10, max=500)
                ], md=6),
            ]),
            dbc.Alert(
                "These parameters control the NSGA-II optimization algorithm. "
                "Higher values may yield better Pareto diversity but increase computation time.",
                color="secondary", className="mt-3 mb-0 small text-center"
            ),
        ])
    ], className="shadow-sm mb-3 h-100")

    # ===============================================================
    # --- Run Button + Spinner abaixo ---
    # ===============================================================
    run_card = dbc.Card([
        dbc.CardBody([
            html.Div([
                dbc.Button(
                    "Run Optimization",
                    id="btn-run-optimization",
                    color="primary",
                    size="lg",
                    className="px-5 py-2"
                ),
            ], className="text-center w-100"),
            html.Br(),
            # Spinner logo abaixo do botão, monitorando o opt-status
            dcc.Loading(
                id="loading-optimization",
                type="default",
                color="#0d6efd",
                className="mt-3",
                children=[
                    html.Div(
                        id="opt-status",
                        className="text-secondary fw-semibold mt-1 text-center"
                    )
                ]
            ),
        ])
    ], className="shadow-sm mb-4")

    # ===============================================================
    # --- Results (Gráfico + Tabela) ---
    # ===============================================================
    results_card = dbc.Card([
        dbc.CardHeader("Optimization Results", className="bg-light fw-bold text-dark"),
        dbc.CardBody([
            html.P(
                "Interactive Pareto Front (Temperature Uniformity vs Treatment Time vs Average Tumor Temperature)",
                className="text-secondary mb-2"
            ),
            dcc.Graph(
                id="opt-pareto-graph",
                style={"height": "600px"}
            ),
            html.Hr(),
            html.P("Top Solutions", className="text-secondary mb-1"),
            dash_table.DataTable(
                id="opt-results-table",
                columns=[
                    {"name": "vf (%)", "id": "vf(%)", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "H (A/m)", "id": "H(A/m)", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "f (Hz)", "id": "f(Hz)", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "r (nm)", "id": "r_nm", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "TAVG (°C)", "id": "TAVG(°C)", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "TMIN (°C)", "id": "TMIN(°C)", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "TC (°C)", "id": "TC(°C)", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "TSTD (°C)", "id": "TSTD", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "Treatment Time (s)", "id": "S_TIME(s)", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "SAR (W/kg)", "id": "SAR(W/kg)", "type": "numeric", "format": {"specifier": ".2f"}},
                    {"name": "RAF (mm)", "id": "RAF(mm)", "type": "numeric", "format": {"specifier": ".2f"}},
                ],
                sort_action="native",
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 'fontSize': 13},
                page_size=8,
                style_header={'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'},
            ),
        ])
    ], className="shadow-sm mb-4")

    # ===============================================================
    # --- LAYOUT FINAL ---
    # ===============================================================
    layout = html.Div([
        dbc.Container([
            html.H3("AI4HyperTherm – Optimization Module", className="fw-bold text-center mb-4"),
            html.P(
                "This module helps design safer and more effective magnetic hyperthermia treatments. "
                "It finds the optimal combination of magnetic parameters to achieve uniform and efficient "
                "tumor heating, while keeping both maximum central and minimum tumor temperatures within "
                "safe clinical limits.",
                className="text-center text-secondary mb-4"
            ),

            # ----------- Cards de parâmetros em duas colunas ----------
            dbc.Row([
                dbc.Col([
                    patient_card,
                    constraints_card
                ], md=6, className="d-flex flex-column justify-content-between"),

                dbc.Col([
                    nanoparticle_card,
                    optimization_card
                ], md=6, className="d-flex flex-column justify-content-between"),
            ], className="g-4 mb-3", align="stretch"),

            # ----------- Botão + Spinner logo abaixo ------------------
            dbc.Row([
                dbc.Col([run_card], width=12, className="text-center")
            ]),

            # ----------- Resultados (gráfico + tabela) ----------------
            dbc.Row([
                dbc.Col([results_card], md=12)
            ]),
        ], fluid=True, className="p-4 bg-white text-dark")
    ])

    return layout
