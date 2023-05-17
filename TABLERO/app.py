#Importamos las librerias necesarias
import os
import dash
import dash
from dash import dcc
from dash import html
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sqlalchemy as sqlal
import psycopg2
import numpy as np
#Nos conectamos a la base de datos y solicitamos los datos para el mapa cloropethico
env_path='env\\app.env'
# load env 
load_dotenv(dotenv_path=env_path)
# extract env variables
USER=os.environ.get('USUARIO')
PASSWORD=os.getenv('CLAVE')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
DBNAME=os.getenv('DBNAME')
#Creamos la conexion
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(USER, PASSWORD, HOST, PORT, DBNAME))
dbConnection=engine.connect();
print("conexion a db ok!")
#Hacemos la consulta
datos_dep=pd.read_sql("SELECT * FROM datos_departamento", dbConnection)#Este es el dataframe con los datos para la visualizacion del mapa

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
    style={'width': '47.5%', 'display': 'inline-block','verticalAlign': 'top',"border":"1px gray ridge"}

    ),
    #Ubicamos un DIV para separar las dos secciones del tablero
    html.Div(#Este div lo usamos para ubicar las listas desplegables del modelo de prediccion y la salida del mismo
    children=[
        #NO UBICAR NADA AQUI, ES SOLO PARA DEJAR ESPACIO ENTRE EL LADO DERECHOY EL IZQUIERDO DEL TABLERO
    ],
    style={'width': '5%', 'display': 'inline-block','verticalAlign': 'top'}),




    html.Div(#Este div lo usamos para ubicar las listas desplegables del modelo de prediccion y la salida del mismo
    children=[
        
    ],
    style={'width': '47.5%', 'display': 'inline-block','verticalAlign': 'top',"border":"1px gray ridge"}
    )
])



if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
 
