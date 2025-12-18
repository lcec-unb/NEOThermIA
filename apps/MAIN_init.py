import sys
import os
from threading import Timer
import webbrowser

sys.path.append(os.path.join(os.path.dirname(__file__), "apps"))


########################################################################################################################
# Import Python Files
########################################################################################################################
from apps.MAIN_apps_list import *
from layouts.layouts_list import *
from main import app
from apps.config import *

#######################################################################################################################
# Layout Principal
#######################################################################################################################
app.layout = html.Div([
    #
    # ======= LOGO FIXO NO TOPO =======
    #
    html.Div([
        html.Img(
            src='assets/logo.png',
            style={
                'width': '100%',          # mantenho como estava
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'zIndex': '1000'
            }
        ),
    ],
    # barra do logo (fixa). Se seu logo tem fundo transparente, vale pôr bg.
    style={
        'textAlign': 'center',
        'height': '100px',             # altura "estimada" do bloco do logo
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'right': '0',
        'backgroundColor': '#f5f5f0',  # combina com o fundo
    }),

    #
    # ======= CONTEÚDO EM COLUNA (CIMA/BAIXO) =======
    #
    html.Div([
        #
        # --- SEÇÃO DE CIMA (antes: coluna esquerda) ---
        #
        # --- SEÇÃO DE CIMA (antes: coluna esquerda) ---
        html.Div([
            dcc.Tabs(
                id='tabs',
                value='TAB_Simulation',
                children=[
                    dcc.Tab(
                        label='Simulation', value='TAB_Simulation', id='TAB_Simulation',
                        style=styles_dict['Simulation']['style_visible'],
                        selected_style=styles_dict['Simulation']['selected_style']
                    ),
                    dcc.Tab(
                        label='Optimization', value='TAB_Optimization', id='TAB_Optimization',
                        style=styles_dict['Optimization']['style_visible'],
                        selected_style=styles_dict['Optimization']['selected_style']
                    ),
                    dcc.Tab(
                        label='Help', value='TAB_Help', id='TAB_Help',
                        style=styles_dict['Help']['style_visible'],
                        selected_style=styles_dict['Help']['selected_style']
                    ),
                    dcc.Tab(
                        label='About', value='TAB_About', id='TAB_About',
                        style=styles_dict['About']['style_visible'],
                        selected_style=styles_dict['About']['selected_style']
                    ),
                ],
                style={
                    'display': 'flex',
                    'flexDirection': 'row',  # lado a lado (horizontal)
                    'justifyContent': 'center',  # centraliza na tela
                    'alignItems': 'center',
                    'gap': '30px',  # espaçamento lateral entre as tabs
                    'margin': '0 auto',
                    'padding': '10px',
                }
            ),
        ],
            style={
                'width': '100%',
                'display': 'flex',
                'justifyContent': 'center',
                'padding': '10px',
                'boxSizing': 'border-box',
            }),

        #
        # --- SEÇÃO DE BAIXO (antes: coluna direita) ---
        #
        html.Div(
            id='tabs-content',
            style={
                'width': '100%',
                'padding': '20px',
                'border': '1px solid #ccc',
                'borderRadius': '10px',
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
                'overflowY': 'auto',
                'minHeight': '40vh',
                # ocupa a tela, descontando a área do logo + margens internas
                'height': 'calc(100vh - 160px)',
                'backgroundColor': '#fcfcf8'
            }
        ),
    ],
    # CONTAINER PRINCIPAL EM COLUNA
    style={
        'display': 'flex',
        'flexDirection': 'column',     # <<< chave para "cima/baixo"
        'gap': '20px',                 # espaço entre as duas seções
        'padding': '10px 10px 20px 10px',
        'boxSizing': 'border-box',
        # cria espaço para não ficar por baixo do logo fixo
        'paddingTop': '120px',         # ajuste se seu logo for mais/menos alto
    }),

    # Store para dados de sessão, etc.
    dcc.Store(id='store-data'),
],
style={'backgroundColor': '#f5f5f0'})

#######################################################################################################################
# Importar Callbacks
#######################################################################################################################

# =============================================================================
# Abrir Navegador automaticamente
# =============================================================================
DefaultIP = '127.0.0.1'
Browser = f'http://{DefaultIP}:{PORT}/'

def open_browser():
    webbrowser.open_new(Browser)

def RUN_NEOThermIA():
    import platform
    if platform.system() != "Linux":
        Timer(1, open_browser).start()
    app.run(host=DefaultIP, port=PORT, debug=False)
