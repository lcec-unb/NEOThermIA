import os
import sys
import dash
import dash_bootstrap_components as dbc
import warnings


warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Configuração do servidor Flask
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

software = "NEOThermIA"
app.title = software
server = app.server

from apps.MAIN_init import *
import apps.MAIN_callbacks

if __name__ == '__main__':
    RUN_NEOThermIA()