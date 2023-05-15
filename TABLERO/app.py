#Importamos las librerias necesarias
import os
import dash
import dash
from dash import dcc
from dash import html
import pandas as pd
import geopandas as gpd
import plotly.express as px







#Los periodos disponibles
periodos = [20194, 20142, 20151, 20162, 20172, 20201, 20224, 20171, 20211,20181, 20161, 20152, 20191]
#el servidor:
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Resultados icfes saber 11'
server = app.server
#la aplicacion:
app.layout = html.Div([
    html.Div(children=[
    html.Div(children=[html.Img(src="assets/icfes.png",style={'width': '60%', 'float': 'left','padding': '5px','display': 'block'})],
    style={'width': '25%', 'display': 'inline-block','verticalAlign': 'top'}),
    html.Div(children=[html.H1("Resultados ICFES Saber 11 - consolidado", style={'font-size':80,'color': 'blue','font-family': 'cursive','textAlign': 'left',
    'verticalAlign': 'center', 'margin-left': 'auto'})],
    style={'width': '75%', 'display': 'inline-block','verticalAlign': 'top'}),  
        
    ])
])



if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
 
