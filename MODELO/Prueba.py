import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import SelectKBest
import os
import sys
pythonPath = os.path.abspath(__file__)
modelPath=os.path.dirname(pythonPath)
print(modelPath)
csv_path=os.path.join(modelPath,"set_10000.csv")
print(csv_path)
datos=pd.read_csv(csv_path)


datosLimpios=datos.dropna()
print(len(datosLimpios))


#Pasar los datos de texto a numerico
datosLimpios.loc["Una"==datosLimpios["fami_personashogar"],"fami_personashogar"]=1
datosLimpios.loc["Dos"==datosLimpios["fami_personashogar"],"fami_personashogar"]=2
datosLimpios.loc["Tres"==datosLimpios["fami_personashogar"],"fami_personashogar"]=3
datosLimpios.loc["Cuatro"==datosLimpios["fami_personashogar"],"fami_personashogar"]=4
datosLimpios.loc["Cinco"==datosLimpios["fami_personashogar"],"fami_personashogar"]=5
datosLimpios.loc["Seis"==datosLimpios["fami_personashogar"],"fami_personashogar"]=6
datosLimpios.loc["Siete"==datosLimpios["fami_personashogar"],"fami_personashogar"]=7
datosLimpios.loc["Ocho"==datosLimpios["fami_personashogar"],"fami_personashogar"]=8
datosLimpios.loc["Nueve"==datosLimpios["fami_personashogar"],"fami_personashogar"]=9
datosLimpios.loc["Diez"==datosLimpios["fami_personashogar"],"fami_personashogar"]=10
datosLimpios.loc["Once"==datosLimpios["fami_personashogar"],"fami_personashogar"]=11
#Intervalos de texto a numerico (Se escoge el máximo)
datosLimpios.loc["5 a 6"==datosLimpios["fami_personashogar"],"fami_personashogar"]=6
datosLimpios.loc["3 a 4"==datosLimpios["fami_personashogar"],"fami_personashogar"]=4
datosLimpios.loc["1 a 2"==datosLimpios["fami_personashogar"],"fami_personashogar"]=2
datosLimpios.loc["7 a 8"==datosLimpios["fami_personashogar"],"fami_personashogar"]=8
datosLimpios.loc["9 o más"==datosLimpios["fami_personashogar"],"fami_personashogar"]=10
datosLimpios.loc["Doce o más"==datosLimpios["fami_personashogar"],"fami_personashogar"]=12
#No se sabe si hay mas datos raros en el arvhivo grande
datosLimpios["fami_personashogar"] = datosLimpios["fami_personashogar"].astype("int")
condicionPersonasHogar = ~(datosLimpios["fami_personashogar"].apply(lambda x: isinstance(x, int)) & 
                           (datosLimpios["fami_personashogar"] >= 1) & 
                           (datosLimpios["fami_personashogar"] <= 12))
datosLimpios = datosLimpios.drop(datosLimpios[condicionPersonasHogar].index)
print(datosLimpios[condicionPersonasHogar].index)
print(len(datosLimpios))

#Verificacion
print("fami_personashogar")
for i in datosLimpios["fami_personashogar"].unique():
    print(i)


#Pasar los datos de texto a numerico
#Intervalos de texto a numerico (Se escoge el máximo)
datosLimpios.loc["Uno"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=1
datosLimpios.loc["Dos"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=2
datosLimpios.loc["Tres"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=3
datosLimpios.loc["Cuatro"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=4
datosLimpios.loc["Cinco"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=5
datosLimpios.loc["Seis"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=6
datosLimpios.loc["Seis o mas"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=7
datosLimpios.loc["Siete"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=7
datosLimpios.loc["Ocho"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=8
datosLimpios.loc["Nueve"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=9
datosLimpios.loc["Diez"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=10  
datosLimpios.loc["Diez o más"==datosLimpios["fami_cuartoshogar"],"fami_cuartoshogar"]=11
#No se sabe si hay mas datos raros en el arvhivo grande
datosLimpios["fami_cuartoshogar"] = datosLimpios["fami_cuartoshogar"].astype("int")
condicionCuartosHogar = ~(datosLimpios["fami_cuartoshogar"].apply(lambda x: isinstance(x, int)) & 
                           (datosLimpios["fami_cuartoshogar"] >= 1) & 
                           (datosLimpios["fami_cuartoshogar"] <= 11))
datosLimpios = datosLimpios.drop(datosLimpios[condicionCuartosHogar].index)
#Verificacion
print("fami_cuartoshogar")
for i in datosLimpios["fami_cuartoshogar"].unique():
    print(i)

for i in datosLimpios.columns:
    print(i)
    print(datosLimpios[i].unique())

datosLimpios.loc["Si"==datosLimpios["fami_tieneautomovil"],"fami_tieneautomovil"]=True
datosLimpios.loc["No"==datosLimpios["fami_tieneautomovil"],"fami_tieneautomovil"]=False
datosLimpios["fami_tieneautomovil"] = datosLimpios["fami_tieneautomovil"].astype("bool")