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
csv_path=os.path.join(modelPath,"datos_limpios.csv")
datosLimpios=pd.read_csv(csv_path)

Y=datosLimpios.loc[:, datosLimpios.columns == "punt_global"]
X=datosLimpios.loc[:, datosLimpios.columns != "punt_global"]
X_train, X_validation, Y_train, Y_validation = \
train_test_split(X, Y, test_size=0.2, random_state=seed)
kfold = KFold(n_splits=3, random_state=seed)
param_grid={'n_estimators':[100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 650, 700, 750, 800, 850, 900, 950, 
            1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500,
            8000, 8500, 9000, 9500, 10000],
            'max_depth':[5,10,15,20]}
model = RandomForestRegressor()
grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring="r2", \
cv=kfold)
grid_result = grid.fit(X_train, Y_train)