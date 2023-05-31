#Importamos las librerias necesarias
import os
import dash
import dash
from dash import dcc
from dash import html
from dash import Dash, Input, Output, State
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
from pickle import load
#Nos conectamos a la base de datos y solicitamos los datos para el mapa cloropethico
featureNames=['fami_personashogar', 'fami_cuartoshogar', 'fami_tieneautomovil', 
              'fami_tienecomputador', 'fami_tieneinternet', 'RURAL', 'URBANO', 
              'No_Bilingue', 'Si_Bilingue', 'Calendario A', 'Calendario B', 
              'Calendario OTRO', 'Caracter ACADÉMICO', 'Caracter TÉCNICO', 
              'Caracter NO APLICA', 'Caracter TÉCNICO/ACADÉMICO', 'Departamento AMAZONAS', 
              'Departamento ANTIOQUIA', 'Departamento ARAUCA', 'Departamento ATLANTICO', 
              'Departamento BOGOTA', 'Departamento BOLIVAR', 'Departamento BOYACA', 
              'Departamento CALDAS', 'Departamento CAQUETA', 'Departamento CASANARE', 
              'Departamento CAUCA', 'Departamento CESAR', 'Departamento CHOCO', 'Departamento CORDOBA', 
              'Departamento CUNDINAMARCA', 'Departamento GUAINIA', 'Departamento GUAVIARE', 
              'Departamento HUILA', 'Departamento LA GUAJIRA', 'Departamento MAGDALENA', 
              'Departamento META', 'Departamento NARIÑO', 'Departamento NORTE SANTANDER', 
              'Departamento PUTUMAYO', 'Departamento QUINDIO', 'Departamento RISARALDA', 
              'Departamento SAN ANDRES', 'Departamento SANTANDER', 'Departamento SUCRE', 
              'Departamento TOLIMA', 'Departamento VALLE', 'Departamento VAUPES', 'Departamento VICHADA', 
              'Colegio Genero FEMENINO', 'Colegio Genero MASCULINO', 'Colegio Genero MIXTO', 
              'Jornada COMPLETA', 'Jornada MAÑANA', 'Jornada NOCHE', 'Jornada SABATINA', 
              'Jornada TARDE', 'Jornada UNICA', 'Naturaleza NO OFICIAL', 'Naturaleza OFICIAL', 
              'Educacion Madre Educación profesional completa', 'Educacion Madre Educación profesional incompleta', 
              'Educacion Madre Ninguno', 'Educacion Madre No Aplica', 'Educacion Madre No sabe', 
              'Educacion Madre Postgrado', 'Educacion Madre Primaria completa', 'Educacion Madre Primaria incompleta', 
              'Educacion Madre Secundaria (Bachillerato) completa', 'Educacion Madre Secundaria (Bachillerato) incompleta', 
              'Educacion Madre Técnica o tecnológica completa', 'Educacion Madre Técnica o tecnológica incompleta', 
              'Educacion Padre Educación profesional completa', 'Educacion Padre Educación profesional incompleta', 
              'Educacion Padre Ninguno', 'Educacion Padre No Aplica', 'Educacion Padre No sabe', 'Educacion Padre Postgrado', 
              'Educacion Padre Primaria completa', 'Educacion Padre Primaria incompleta', 
              'Educacion Padre Secundaria (Bachillerato) completa', 'Educacion Padre Secundaria (Bachillerato) incompleta', 
              'Educacion Padre Técnica o tecnológica completa', 'Educacion Padre Técnica o tecnológica incompleta', 
              'Genero Estudiante F', 'Genero Estudiante M', 'Estrato 1', 'Estrato 2', 
              'Estrato 3', 'Estrato 4', 'Estrato 5', 'Estrato 6', 'Sin Estrato']
pythonPath = os.path.abspath(__file__)
modelPath=os.path.dirname(pythonPath)
serializedModelPath=os.path.join(modelPath,"modelo_serializado2.sav")
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
                    
                   color_continuous_scale='Blues',
                        labels=labels_1,
                        
                   hover_data =hover,
                   scope='south america',
                   height=1000)
    fig.update_geos(fitbounds="locations", visible=True)#
    fig.update_layout(
        title_text='Resultados de pruebas saber 11 periodo '+str(periodo)
    )
    fig.update(layout = dict(title=dict(x=0.5)))
    fig.update_layout(
        autosize=True,
        margin={"r":10,"t":10,"l":10,"b":10,'autoexpand':True},
        coloraxis_colorbar={
            'title':"""{} del puntaje global""".format(dict_drop[opcion]),
            'orientation':'h',
            'len':0.8})
        
    #fig.update_traces(colorbar_orientation='h', selector=dict(type='heatmap'))
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
    html.Div(children=[html.H1("Resultados ICFES Saber 11 - consolidado", style={'font-size':60,'color': 'blue','font-family': 'cursive','textAlign': 'left',
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
        dcc.Graph(id='mapa',figure=colombian_map(df_merged, 20194, 1),style={'width': '45vw', 'height': '151vh'})
       
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
        html.Br(style={"line-height": "40"}),
        #Ubicamos un elemento de texto para indicar la funcion del slider
        html.Label("Ingrese los datos socio-economicos del estudiante para obtener una predicción del desempeño en las pruebas saber 11",
        style={'font-size':'70','font-family': 'cursive'}),
        html.Br(style={"line-height": "30"}),
        html.Label("Departamento de ubicación",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['CHOCO', 'VAUPES', 'AMAZONAS', 'LA GUAJIRA', 'MAGDALENA', 'VICHADA',
       'BOLIVAR', 'GUAINIA', 'CAUCA', 'GUAVIARE', 'SAN ANDRES', 'CAQUETA',
       'CORDOBA', 'CESAR', 'SUCRE', 'PUTUMAYO', 'TOLIMA', 'ARAUCA',
       'ATLANTICO', 'ANTIOQUIA', 'CASANARE', 'META', 'NARIÑO', 'CALDAS',
       'HUILA', 'VALLE', 'QUINDIO', 'RISARALDA', 'NORTE SANTANDER',
       'CUNDINAMARCA', 'BOYACA', 'SANTANDER', 'BOGOTA'], 'BOGOTA', id='drop-departamentos'),
        html.Label("Jornada del colegio",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['NOCHE','SABATINA','MAÑANA','TARDE','COMPLETA','UNICA'], 'UNICA', id='drop-jornada'),
        html.Label("Naturaleza del colegio",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['OFICIAL','NO OFICIAL'], 'OFICIAL', id='drop-naturaleza_cole'),
        html.Label("Genero del colegio",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['MIXTO','MASCULINO','FEMENINO'], 'MIXTO', id='drop-genero_cole'),
        html.Label("Calendario del colegio",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['A','B','OTRO'], 'A', id='drop-calendario'),
        html.Label("Colegio bilingüe?",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['Si','No'], 'Si', id='drop-bilingue'),
        html.Label("Caracter del colegio?",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['Academico','Tecnico','No aplica','Tecnico/Academico'], 'Tecnico', id='drop-caracter'),
        html.Label("Ubicacion del colegio",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['RURAL','URBANO'], 'URBANO', id='drop-ubicacion'),
        html.Label("Numero de personas que conforman el nucleo familiar",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown([1,2,3,4,5,6,7,8,9,10,11,12], '3', id='drop-fami_personas_hogar'),
        html.Label("Número de habitaciones con que cuenta la vivienda del nucleo familiar",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown([1,2,3,4,5,6,7,8,9,10,11,12], '3', id='drop-fami_cuartos_hogar'),
        html.Label("Estrato de la vivienda del nucleo familiar",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['1','2','3','4','5','6','Sin Estrato'], '3', id='drop-estrato'),
        html.Label("La familia cuenta con computador?",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['Si','No'], 'Si', id='drop-computador'),
        html.Label("La familia cuenta con vehiculo propio?",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['Si','No'], 'Si', id='drop-vehiculo'),
        html.Label("La familia cuenta con acceso a internet?",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['Si','No'], 'Si', id='drop-internet'),
        html.Label("Genero del estudiante",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['M','F'], 'M', id='drop-genero_estu'),
        html.Label("Mayor nivel educativo del padre del alumno",style={'font-size':'70','font-family': 'cursive'}),
        dcc.Dropdown(['Secundaria (Bachillerato) completa',
        'Educación profesional completa',
                              'No sabe',
       'Técnica o tecnológica completa',
 'Secundaria (Bachillerato) incompleta',
                  'Primaria incompleta',
                            'Postgrado',
                    'Primaria completa',
                            'No Aplica',
                            'Secundaria (Bachillerato) completa',
                              'Ninguno',
     'Educación profesional incompleta',
     'Técnica o tecnológica incompleta'], 'Educación profesional completa', id='drop-edu_padre'),
     html.Label("Mayor nivel educativo de la madre del alumno",style={'font-size':'70','font-family': 'cursive'}),
     dcc.Dropdown(['Secundaria (Bachillerato) completa',
       'Educación profesional completa',
                              'No sabe',
       'Técnica o tecnológica completa',
 'Secundaria (Bachillerato) incompleta',
                  'Primaria incompleta',
                            'Postgrado',
                    'Primaria completa',
                            'No Aplica',
                              'Ninguno',
     'Educación profesional incompleta',
     'Secundaria (Bachillerato) completa',
     'Técnica o tecnológica incompleta'], 'Educación profesional completa', id='drop-edu_madre'),
    html.Br(style={"line-height": "40"}),
    html.Button('Estimar puntaje global del estudiante', id='calcular', n_clicks=0,style={'font-size': '12px', 
    'width': '100%', 'display': 'inline-block', 
    'margin-bottom': '10px', 'margin-right': '5px', 'height':'37px', 'verticalAlign': 'top'}),
     html.Br(style={"line-height": "40"}),
     html.Label("El puntaje global estimado que el estudiante obtendrá en las pruebas saber es:",style={'font-size':'70','font-family': 'cursive'}),
     dcc.Textarea(
        id='puntaje_estimado',
        value='',
        style={'width': '100%', 'height': '100%'},
    )
    ],
    style={'width': '47.5%', 'display': 'inline-block','verticalAlign': 'top',"border":"1px gray ridge"}
    ),
    html.Div(#Este div los usamos para dejar un margen derecho
        children=[],
        style={'width': '1.5%','display': 'inline-block','verticalAlign': 'top'})
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
#Definimos algunos diccionarios que nos seran utiles para la estimacion del puntaje global
dict_si_true={'Si':True,'No':False}
#Definimos aqui el callback y la funcion que estiman el puntaje global:
my_list_departments=['AMAZONAS','ANTIOQUIA', 'ARAUCA', 'ATLANTICO', 'BOGOTA', 'BOLIVAR', 'BOYACA', 'CALDAS','CAQUETA','CASANARE','CAUCA','CESAR', 
'CHOCO', 'CORDOBA', 'CUNDINAMARCA','GUAINIA','GUAVIARE','HUILA','LA GUAJIRA','MAGDALENA','META','NARIÑO', 'NORTE SANTANDER','PUTUMAYO',
'QUINDIO','RISARALDA', 'SAN ANDRES', 'SANTANDER','SUCRE','TOLIMA', 'VALLE', 'VAUPES', 'VICHADA']
my_list_jornadas=['COMPLETA','MAÑANA','NOCHE','SABATINA','TARDE','UNICA']
my_list_eduacion_padres=['Educación profesional completa',
'Educación profesional incompleta', 'Ninguno', 'No Aplica', 'No sabe', 'Postgrado', 'Primaria completa', 'Primaria incompleta', 
'Secundaria (Bachillerato) completa', 'Secundaria (Bachillerato) incompleta', 'Técnica o tecnológica completa', 'Técnica o tecnológica incompleta'] 
my_list_estratos=['1','2','3','4','5','6','Sin Estrato']     
           
#DEFINIMOS LA FUNCION QUE ESTIMA EL PUNTAJE OBTENIDO POR UN ALUMNO
#            
        
model= load(open(serializedModelPath,'rb'))        
@app.callback(
    Output("puntaje_estimado","value"),
    Input(component_id='calcular', component_property='n_clicks'),
    State(component_id='drop-fami_personas_hogar', component_property='value'),
    State(component_id='drop-fami_cuartos_hogar', component_property='value'),
    State(component_id='drop-vehiculo', component_property='value'),
    State(component_id='drop-computador', component_property='value'),
    State(component_id='drop-internet', component_property='value'),
    State(component_id='drop-ubicacion', component_property='value'),
    State(component_id='drop-bilingue', component_property='value'),
    State(component_id='drop-calendario', component_property='value'),
    State(component_id='drop-caracter', component_property='value'),
    State(component_id='drop-departamentos', component_property='value'),
    State(component_id='drop-genero_cole', component_property='value'),
    State(component_id='drop-jornada', component_property='value'),
    State(component_id='drop-naturaleza_cole', component_property='value'),
    State(component_id='drop-edu_madre', component_property='value'),
    State(component_id='drop-edu_padre', component_property='value'),
    State(component_id='drop-genero_estu', component_property='value'),
    State(component_id='drop-estrato', component_property='value')
)

def estimar_puntaje(n_clicks, fami_personas_hogar, fami_cuartos_hogar, fami_tiene_automovil, fami_tiene_pc,fami_tiene_internet,
ubicacion_rural_urbano, bilingue, calendario, caracter_cole, departamento, genero_colegio, jornada, naturaleza, educacion_madre,
educacion_padre, genero_estudiante, estrato):
    if n_clicks==0:
        return "Oprima el boton para realizar un estimado"
    else:

        lista=[]
        #Añadimos el numero de personas del hogar:
        lista.append(int(fami_personas_hogar))
        #Añadimos el numero de cuartos que tiene el hogar
        lista.append(int(fami_cuartos_hogar))
        #Añadimos si la familia tiene auto
        lista.append(dict_si_true[fami_tiene_automovil])
        #Añadimos si la familia tiene computador
        lista.append(dict_si_true[fami_tiene_pc])
        #Añadimos si la familia tiene internet
        lista.append(dict_si_true[fami_tiene_internet])
        #VERIFICA SI EL COLEGIO ES RURAL O URBANO
        if ubicacion_rural_urbano=='RURAL':
            lista.append(1)
            lista.append(0)
        else:
            lista.append(0)
            lista.append(1)
        #VERIFICA SI EL COLEGIO ES BILINGÜE
        if bilingue=='Si':
            lista.append(0)
            lista.append(1)
        else:
            lista.append(1)
            lista.append(0)
        #VERIFICA EL CALENDARIO ACADEMICO
        if calendario=='A':
            lista.append(1)
            lista.append(0)
            lista.append(0)
        elif calendario=='B':
            lista.append(0)
            lista.append(1)
            lista.append(0)
        else:
            lista.append(0)
            lista.append(0)
            lista.append(1)
        #VERIFICAMOS EL CARACTER DEL COLEGIO
        if caracter_cole=='Academico':
            lista.append(1)
            lista.append(0)
            lista.append(0)
            lista.append(0)
           
        elif caracter_cole=='Tecnico':
            lista.append(0)
            lista.append(1)
            lista.append(0)
            lista.append(0)
          
       
        elif caracter_cole=='No aplica':
            lista.append(0)
            lista.append(0)
            lista.append(1)
            lista.append(0)
            
        elif caracter_cole=='Tecnico/Academico':
            lista.append(0)
            lista.append(0)
            lista.append(0)
            lista.append(1)
          
        #VERIFICAMOS QUE DEPARTAMENTO ES
        indice_departamento=my_list_departments.index(departamento)
        my_new_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        my_new_list[indice_departamento]=1
        for element in my_new_list:
            lista.append(element)
        #Verificamos el genero del colegio
        if genero_colegio=='FEMENINO':
            lista.append(1)
            lista.append(0)
            lista.append(0)
        elif genero_colegio=='MASCULINO':
            lista.append(0)
            lista.append(1)
            lista.append(0)
        else:
            lista.append(0)
            lista.append(0)
            lista.append(1)
        #VERIFICAMOS EL TIPO DE JORNADA
        indice_jornada=my_list_jornadas.index(jornada)
        my_new_list=[0,0,0,0,0,0]
        my_new_list[indice_jornada]=1
        for element in my_new_list:
            lista.append(element)
        #VERIFICAMOS LA NATURALEZA DEL COLEGIO
        if naturaleza=='NO OFICIAL':
            lista.append(1)
            lista.append(0)
        else:
            lista.append(0)
            lista.append(1)
        #VERIFICAMOS LA EDUCACION DE LA MADRE
        indice_ed_madre=my_list_eduacion_padres.index(educacion_madre)
        my_new_list=[0,0,0,0,0,0,0,0,0,0,0,0]
        my_new_list[indice_ed_madre]=1
        for element in my_new_list:
            lista.append(element)
        #VERIFICAMOS LA EDUCACION DEL PADRE
        indice_ed_padre=my_list_eduacion_padres.index(educacion_padre)
        my_new_list=[0,0,0,0,0,0,0,0,0,0,0,0]
        my_new_list[indice_ed_padre]=1
        for element in my_new_list:
            lista.append(element)
        #VERIFICAMOS EL GENERO DEL ESTUDIANTE
        if genero_estudiante=='F':
            lista.append(1)
            lista.append(0)
        else:
            lista.append(0)
            lista.append(1)
        #VERIFICAMOS EL ESTRATO
        indice_estrato=my_list_estratos.index(estrato)
        my_new_list=[0,0,0,0,0,0,0]
        my_new_list[indice_estrato]=1
        for element in my_new_list:
            lista.append(element)
        x=np.reshape(lista,(1,93))
        dfPredictions = pd.DataFrame(x, columns=featureNames)
        predictions=round(model.predict(dfPredictions))
        

        return str(lista)



    return None




if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
 
