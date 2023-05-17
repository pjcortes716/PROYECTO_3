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
periodos = {9:'20194',0:'20142',1:'20151',4:'20162',6:'20172',10:'20201',12:'20224',5:'20171',11:'20211',7:'20181',3:'20161',2:'20152',8:'20191'}     
#el servidor:
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Resultados icfes saber 11'
server = app.server
#la aplicacion:
app.layout = html.Div([#este div es el encabezado del tablero, lo usamos para ubicar el logo del icfes y el nombre del tablero
    html.Div(children=[
    html.Div(children=[html.Img(src="assets/icfes.png",style={'width': '60%', 'float': 'left','padding': '5px','display': 'block'})],
    style={'width': '25%', 'display': 'inline-block','verticalAlign': 'top'}),
    html.Div(children=[html.H1("Resultados ICFES Saber 11 - consolidado", style={'font-size':80,'color': 'blue','font-family': 'cursive','textAlign': 'left',
    'verticalAlign': 'center', 'margin-left': 'auto'})],
    style={'width': '75%', 'display': 'inline-block','verticalAlign': 'top'}),  
        
    ]),
    html.Div(#Este div lo usamos para ubicar la grafica del mapa
    children=[
        html.Br(style={"line-height": "40"}),
        #Ubicamos un elemento de texto para indicar la funcion del slider
        html.Label("Seleccione un periodo de visualizacion",style={'font-size':'70','font-family': 'cursive'}),
        html.Br(style={"line-height": "30"}),
        #Ubicamos la barra deslizante de los periodos
        dcc.Slider(0,12,marks=periodos, value=10,id='barra_periodos',tooltip={"placement": "bottom", "always_visible": True}),
        html.Br(style={"line-height": "30"}),
        #Ubicamos el label que indica la funcion de la lista desplegable
        html.Label("Seleccione un estadistico a visualizar",style={'font-size':'70','font-family': 'cursive'}),
        html.Br(style={"line-height": "30"}),
        dcc.Dropdown(['Promedio', 'Minimo', 'Maximo'], 'Promedio', id='dropdown-estadistico',style={'font-size':'70','font-family': 'cursive'}),
        html.Br(style={"line-height": "30"})
        #A continuacion va el mapa:
        
    ],
    style={'width': '50%', 'display': 'inline-block','verticalAlign': 'top'}

    ),
    html.Div(#Este div lo usamos para ubicar las listas desplegables del modelo de prediccion y la salida del mismo
    children=[],
    style={'width': '50%', 'display': 'inline-block','verticalAlign': 'top'}
    )
])



if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
 
