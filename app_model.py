from fastapi import FastAPI, HTTPException
import uvicorn
import os
import pickle
import pandas as pd
import sqlite3
import numpy as np

df = pd.read_csv('data/Advertising.csv')

app = FastAPI()

# Crear una conexión a una base de datos SQLite en disco
conn = sqlite3.connect('advertising.db')  # Asegúrate de que la extensión es .db
df.to_sql('advertising', conn, if_exists='replace', index=False)




# 1. Endpoint de predicción
@app.get("/predict")
async def prediccion(TV: int, radio: int, newpaper: int):
   
   with open('data/advertising_model.pkl', 'rb') as f:
            model = pickle.load(f)
   data_inversion = {'TV': TV, 'radio': radio, 'newpaper': newpaper}
   input = pd.DataFrame([data_inversion])
   prediction = model.predict(input)
   return {"Prediction": prediction[0]}

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

