#Importamos las librerias necesarias
import os
import dash
import dash
from dash import dcc
from dash import html
from dash import Dash, Input, Output
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sqlalchemy as sqlal
import psycopg2
import numpy as np
import geopandas as gpd
import plotly.express as px
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
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------La función para hacer el mapa-------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
#Importamos las coordenadas de las fronteras de los departamentos
departamentos=gpd.read_file("departamentos_colombi.txt")
departamentos=departamentos[["DPTO","NOMBRE_DPT","geometry"]]
departamentos.DPTO=departamentos.DPTO.astype('int')
#Unimos los dataframes de las coordenadas del departamento con el de los resultados icfes
datos_dep.rename(columns={'codigo_departamento':'DPTO'},inplace=True)
datos_dep=datos_dep.dropna()
datos_dep['DPTO']=datos_dep['DPTO'].astype('int')
df_merged = departamentos.merge(datos_dep, left_on=['DPTO'], right_on=['DPTO'])
#Ahora si la funcion
def colombian_map(df,periodo,opcion):
    dict_drop={1:'Promedio',2:"Maximo",3:'Minimo'}
    if opcion==1:#se grafica la media
        hover=['puntaje_ingles','puntaje_mate', 'puntaje_soc', 'puntaje_nat','puntaje_lec']
        labels_1={'NOMBRE_DPT':"Departamento",'puntaje_mate':'puntaje matematicas','puntaje_soc':'puntaje c.sociales',
                               'puntaje_nat':'puntaje c.naturales','puntaje_lec':'puntaje lectura'}
    elif opcion==2:#Se grafica el maximo puntaje
        hover=['max_p_ingles','max_p_mate','max_p_soc','max_p_nat','max_p_lec','max_p_global']
        labels_1={'NOMBRE_DPT':"Departamento",'max_p_ingles':'Máximo puntaje en ingles','max_p_soc':'Máximo puntaje c.sociales',
                               'max_p_nat':'Máximo puntaje c.naturales','max_p_lec':'Maximo puntaje letura','max_p_global':'Máximo puntaje global',
                               'max_p_mate':'Máximo puntaje matematicas'}
    elif opcion==3:
        hover=['min_p_ingles','min_p_mate','min_p_soc','min_p_nat','min_p_lec','min_p_global']
        labels_1={'NOMBRE_DPT':"Departamento",'min_p_ingles':'Minimo puntaje en ingles','min_p_soc':'Minimo puntaje c.sociales',
                               'min_p_nat':'Minimo puntaje c.naturales','min_p_lec':'Minimo puntaje letura','min_p_global':'Minimo puntaje global',
                               'min_p_mate':'Minimo puntaje matematicas'}
    dict_graph={1:'puntaje_global',2:'max_p_global',3:'min_p_global'}
    df_mod=df[df['periodo']==periodo]
    df_mod=df_mod.set_index("NOMBRE_DPT")
    fig = px.choropleth(df_mod, geojson=df_mod.geometry, 
                    locations=df_mod.index, color=dict_graph[opcion],
                    height=800,
                   color_continuous_scale="Jet",
                        labels=labels_1,
                        
                   hover_data =hover)
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(
        title_text='Resultados de pruebas saber 11 periodo '+str(periodo)
    )
    fig.update(layout = dict(title=dict(x=0.5)))
    fig.update_layout(
        margin={"r":0,"t":30,"l":10,"b":10},
        coloraxis_colorbar={
            'title':"""{} del puntaje global""".format(dict_drop[opcion])})
    return fig
####################################################################################################################################################
#####################################################FIN DE LA FUNCION PARA GENERAR EL MAPA#########################################################

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
    html.Div(#Este div los usamos para dejar un margen izquierdo
        children=[],
        style={'width': '1.5%', 'display': 'inline-block','verticalAlign': 'top'}),
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
        html.Br(style={"line-height": "30"}),
        #A continuacion va el mapa:
        dcc.Graph(id='mapa',figure=colombian_map(df_merged, 20194, 1),style={'width': '45vw', 'height': '65vh'})
    ],
    style={'width': '47.5%', 'display': 'inline-block','verticalAlign': 'top',"border":"1px gray ridge"}

    ),
    #Ubicamos un DIV para separar las dos secciones del tablero
    html.Div(#
    children=[
        #NO UBICAR NADA AQUI, ES SOLO PARA DEJAR ESPACIO ENTRE EL LADO DERECHOY EL IZQUIERDO DEL TABLERO
    ],
    style={'width': '3%', 'display': 'inline-block','verticalAlign': 'top'}),




    html.Div(#Este div lo usamos para ubicar las listas desplegables del modelo de prediccion y la salida del mismo
    children=[
        
    ],
    style={'width': '47.5%', 'display': 'inline-block','verticalAlign': 'top',"border":"1px gray ridge"}
    ),
    html.Div(#Este div los usamos para dejar un margen derecho
        children=[],
        style={'width': '1.5%', 'display': 'inline-block','verticalAlign': 'top'})
])
#diccionario de opciones del dropdown
dict_drop={'Promedio':1,"Maximo":2,'Minimo':3}
#callback de la grafica
@app.callback(
    Output(component_id='mapa', component_property='figure'),
    Input(component_id='barra_periodos', component_property='value'),
    Input(component_id='dropdown-estadistico', component_property='value')
)
def update_map(input_value,estadistico):
    value=int(input_value)
    periodo=periodos[value]
    periodo=int(periodo)
    opcion=dict_drop[estadistico]
    fig=colombian_map(df_merged,periodo,opcion)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
 
