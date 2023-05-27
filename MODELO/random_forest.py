import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from pickle import dump
from pickle import load

import os
import sys
pythonPath = os.path.abspath(__file__)
modelPath=os.path.dirname(pythonPath)
csv_path=os.path.join(modelPath,"datos_limpios.csv")
datosLimpios=pd.read_csv(csv_path)
seed=3
Y=datosLimpios.loc[:, datosLimpios.columns == "punt_global"]
print(Y)
X=datosLimpios.loc[:, datosLimpios.columns != "punt_global"]
X_train, X_validation, Y_train, Y_validation = \
train_test_split(X, Y, test_size=0.2, random_state=seed)
Y_train = Y_train.values.ravel()
kfold = KFold(n_splits=3, random_state=seed, shuffle=True,)
param_grid={'n_estimators':[100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 650, 700, 750, 800, 850, 900, 950,
                            1000],'max_depth':[5,10,15,20,25,30]}

            
model = RandomForestRegressor()
grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring="r2", \
cv=kfold)
grid_result = grid.fit(X_train, Y_train)
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
print(grid_result.best_params_)
print(grid_result.best_params_["max_depth"])
print(grid_result.best_params_["n_estimators"])

bestModel=RandomForestRegressor(n_estimators=grid_result.best_params_["n_estimators"], max_depth=grid_result.best_params_["max_depth"])
bestModel.fit(X_train, Y_train)
predictionsTrain = bestModel.predict(X_train)
print(r2_score(Y_train, predictionsTrain))

predictionsTest = bestModel.predict(X_validation)
print(mean_squared_error(Y_validation, predictionsTest))
print(r2_score(Y_validation, predictionsTest))

filename=os.path.join(modelPath,"modelo_serializado.sav")
dump(bestModel, open(filename, "wb"))