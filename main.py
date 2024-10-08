import http
import json
from http.client import HTTPException
import pandas as pd
import os
from dotenv import load_dotenv


from fastapi import FastAPI

import requests
import json
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

# Definición del modelo de datos
class Registro(BaseModel):
    Title: str
    Content: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

API_KEY = os.environ.get('Api_Key')

@app.get("/get_records/")
def get_records():
    try:
        # Verifica que la variable de entorno 'getapi' esté configurada
        api_url = os.environ.get('getapi')
        print("getapi:", api_url)
        if api_url is None:
            raise ValueError("La variable de entorno 'getapi' no está configurada.")

        # Verifica que la variable de entorno 'API_KEY' esté configurada
        api_key = os.environ.get('API_KEY')
        if api_key is None:
            raise ValueError("La variable de entorno 'API_KEY' no está configurada.")

        # Establece la conexión HTTPS con la API de NoCoDB
        conn = http.client.HTTPSConnection("app.nocodb.com")

        # Encabezados con el token de autenticación
        headers = {'xc-token': api_key}

        # Realizar la solicitud GET
        conn.request("GET", api_url, headers=headers)

        # Obtener la respuesta
        res = conn.getresponse()
        data = res.read()
        lista = data.decode("utf-8")

        # Verifica si la respuesta es JSON
        try:
            json_object = json.loads(lista)
        except json.JSONDecodeError:
            raise HTTPException(500, "Failed to decode JSON response: " + lista)

        # Inicializar la variable cadenaasistentes
        cadenaasistentes = []

        # Recorrer el diccionario y obtener la lista de registros
        for clave in json_object:
            if clave == "list":
                cadenaasistentes = json_object[clave]

        # Convertir a DataFrame
        if cadenaasistentes:
            df = pd.DataFrame(cadenaasistentes, columns=['Title', 'Content'])
            return df.to_dict(orient="records")
        else:
            return {"message": "No data available."}

    except ValueError as ve:
        print("Error de configuración:", str(ve))  # Debugging
        raise HTTPException(500, str(ve))
    except Exception as e:
        print("Error:", str(e))  # Debugging
        raise HTTPException(500, str(e))

@app.post("/create_record/")
def create_record(record: dict):
    try:
        api_url = os.environ.get('postapi')
        api_key = os.environ.get('API_KEY')

        if api_url is None:
            raise HTTPException(500, "La variable de entorno 'postapi' no está configurada.")
        if api_key is None:
            raise HTTPException(500, "La variable de entorno 'API_KEY' no está configurada.")

        headers = {'xc-token': api_key, 'Content-Type': 'application/json'}
        response = requests.post(api_url, json=record, headers=headers)

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return response.json()
    except Exception as e:
        raise HTTPException(500, str(e))