import http
import json
from http.client import HTTPException
import pandas as pd


from fastapi import FastAPI

import requests
import json
from pydantic import BaseModel

app = FastAPI()

# Definición del modelo de datos
class Registro(BaseModel):
    Title: str
    Content: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

API_KEY = "Req04A-Id0HJN2xcVlAEZiOAP6IYlTgGES3ySakg"

@app.get("/get_records/")
def get_records():
    try:
        # Establece la conexión HTTPS con la API de NoCoDB
        conn = http.client.HTTPSConnection("app.nocodb.com")

        # Encabezados con el token de autenticación
        headers = {'xc-token': API_KEY}  # Asegúrate de reemplazar con tu API Key

        # Realizar la solicitud GET
        conn.request("GET", "/api/v2/tables/m1dcf9vabgqnrun/records?offset=0&limit=25&where=&viewId=vwjsp4cdzqklgf3b", headers=headers)

        # Obtener la respuesta
        res = conn.getresponse()
        data = res.read()
        lista = data.decode("utf-8")
        print("Respuesta de la API:", lista)  # Debugging

        # Cargar JSON a un objeto Python
        json_object = json.loads(lista)
        print("Objeto JSON:", json_object)  # Debugging

        # Inicializar la variable cadenaasistentes
        cadenaasistentes = []

        # Recorrer el diccionario y obtener la lista de registros
        for clave in json_object:
            if clave == "list":
                cadenaasistentes = json_object[clave]
                print("Lista de asistentes:", cadenaasistentes)  # Debugging

        # Convertir a DataFrame
        if cadenaasistentes:
            df = pd.DataFrame(cadenaasistentes, columns=['Title', 'Content'])
            print("DataFrame:", df)  # Debugging
            return df.to_dict(orient="records")
        else:
            return {"message": "No data available."}

    except Exception as e:
        print("Error:", str(e))  # Debugging
        raise HTTPException(500, str(e))

@app.post("/create_record/")
def create_record(registro: Registro):
    try:

        api_url = "https://app.nocodb.com/api/v2/tables/m1dcf9vabgqnrun/records"

        headers = {
            'xc-token': API_KEY,
            'Content-Type': "application/json"
        }

        response = requests.post(api_url, data=registro.json(), headers=headers)

        # Verifica si la solicitud fue exitosa
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))