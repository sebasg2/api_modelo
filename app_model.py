from fastapi import FastAPI, HTTPException
import numpy as np
import uvicorn
import os
import pickle
import pandas as pd
import sqlite3

# Leer el archivo CSV
df = pd.read_csv('data/advertising.csv')

df.drop(columns='Unnamed: 0',axis=1,inplace=True)
print(df.dtypes)

# Crear una conexión a una base de datos SQLite en disco
conn = sqlite3.connect('advertising.db')  # Asegúrate de que la extensión es .db
df.to_sql('advertising', conn, if_exists='replace', index=False)

app = FastAPI()

import pickle

# Load the model
with open('data/advertising_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Print the type of the model
print(type(model))

# Print the model's attributes and methods
print(dir(model))

# 1. Endpoint de predicción
@app.get("/predict/")
async def predict(tv: float, radio: float, newspaper: float):
    
    with open('data/advertising_model.pkl', 'rb') as f:
        model = pickle.load(f)
   
    
    input_data = np.array([[tv, radio, newspaper]])
    predictions = model.predict(input_data)

    
    return predictions

# 2. Endpoint de ingesta de datos

@app.post("/ingesta/")
async def ingesta(TV: float, radio: float, newpaper: float, sales: float):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO advertising (TV, radio, newpaper, sales) VALUES (?, ?, ?, ?)",
                   (TV, radio, newpaper, sales))
    conn.commit()
    cursor.close()
    return {"message": "Datos insertados"}





# Endpoint para reentrenar
@app.get("/retrain/")
async def retrain():
   
   with open('data/advertising_model.pkl', 'rb') as f:
    model = pickle.load(f)
    
    # Sacar los nuevos datos
    cursor = conn.cursor()
    cursor.execute("SELECT TV, radio, newpaper, sales FROM advertising")
    results = cursor.fetchall()
    cursor.close()

    # Separar en X e y
    X = np.array([list(row[:-1]) for row in results])  # Features
    y = np.array([row[-1] for row in results])        # Target

        # Reentrenamiento
    model.fit(X, y)

        # Volver a guardar
    with open('data/advertising_model.pkl', 'wb') as f:
            pickle.dump(model, f)
    return {"message": "Modelo reentrenado"}

 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
   

