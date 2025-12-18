import sys
import os
from dash import html


def layout_help():
    layout = html.Div([
        html.Iframe(id='html-viewer', src='assets/html_help/index.html',
                    style={'width': '100%', 'height': '800px', 'margin': 'auto',
                           'text-align': 'center', 'display': 'flex', 'justify-content': 'center'})
    ], style = {'background-color': '#fcfcf8'})
    return layout
