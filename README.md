# API de Predicción de Ventas (Advertising)

Este proyecto implementa una API usando FastAPI que permite predecir las ventas basado en los gastos en TV, radio y periódicos utilizando un modelo ML. 
También incluye funcionalidades para la ingestión de datos en una base de datos SQLite y el reentrenamiento del modelo con nuevos datos

## Predicción de Ventas

- **URL:** `http://localhost:8000/predict`
- **Método HTTP:** GET
- **Parámetros de Consulta:**
  - `TV`: Gasto en publicidad en TV (entero)
  - `radio`: Gasto en publicidad en radio (entero)
  - `newpaper`: Gasto en publicidad en periódicos (entero)
- **Respuesta:** Retorna la predicción de ventas basada en los datos ingresados.

## Ingesta de Datos

- **URL:** `http://localhost:8000/ingesta`
- **Método HTTP:** POST
- **Cuerpo de la Solicitud (JSON):**
  ```json
  {
    "TV": valor,
    "radio": valor,
    "newpaper": valor,
    "sales": valor
  }
Respuesta: Retorna un mensaje confirmando que los datos han sido insertados en la base de datos.
## Reentrenamiento del Modelo
_**URL:** http://localhost:8000/retrain
-**Método HTTP:** GET
-**Respuesta**: Retorna un mensaje indicando que el modelo ha sido reentrenado con éxito usando los datos más recientes de la base de datos.
