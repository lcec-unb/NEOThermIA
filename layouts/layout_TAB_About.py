import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from datetime import datetime

def layout_TAB_About():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    layout = html.Div([
        html.Iframe(
            id='pdf-viewer',
            src=f"/assets/BR512025006616-3.pdf?{timestamp}#page=1&zoom=page-width",
            style={
                'width': '100%',
                'height': '100vh',  # ocupa toda a altura da tela
                'margin': '0',
                'padding': '0',
                'border': 'none',
            }
        ),
    ], style={'height': '100vh', 'width': '100%'})  # garante que o container também ocupe a tela
    return layout
