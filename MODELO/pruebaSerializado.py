from pickle import load
import pandas as pd
import os


pythonPath = os.path.abspath(__file__)
modelPath=os.path.dirname(pythonPath)
serializedModelPath=os.path.join(modelPath,"modelo_serializado2.sav")
model= load(open(serializedModelPath,'rb'))
csv_path=os.path.join(modelPath,"datos_limpios.csv")
datos=pd.read_csv(csv_path)
featureNames=datos.columns.tolist()
featureNames.remove('punt_global')

print(len(featureNames))
sample=[[3, 3, True, True, True, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]]
print(len(sample))
df = pd.DataFrame(sample, columns=featureNames)
predictions=model.predict(df)
print(predictions)
print(featureNames)