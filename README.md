# Guía para desplegar FastAPI en Render usando NocoDB (base de datos relacional):

**Requisitos para realizar este procedimiento:**
	* **NOTA**: Es necesario que todos los registros los realice con las credenciales de github, en especial Render. Si alguno no deja realizar el registro de esta manera, puede realizarlo con otro correo electrónico.

1. Tener una cuenta en Noco DB
2. Tener una cuenta en render
3. Tener un entorno de Desarrollo Python
4. Tener una cuenta en Github
* Nota: Si no tiene ninguna de las anteriores, puede acceder a las siguientes documentaciones para poder iniciar con este proyecto educativo:
	* Registrarse en Render: https://dashboard.render.com/register
	* Leer la Documentación de Render: https://render.com/docs
	* Registrarse en NocoDB: https://www.nocodb.com/
	* Leer la Documentación de Noco DB: https://docs.nocodb.com/
	* Descargar e Instalar Python en el Dispositivo: https://www.python.org/downloads/
	* Leer la Documentación de Python: https://docs.python.org/3/
	* Guía de uso de PIP: https://pip.pypa.io/en/stable/installation/
	* Documentación de FastAPI: https://fastapi.tiangolo.com/
	* Documentación de Uvicorn: https://www.uvicorn.org/
	* Documentación de Pandas: https://pandas.pydata.org/pandas-docs/stable/
	* Documentación de Requests: https://docs.python-requests.org/en/latest/
	* Documentación oficial de Git: [https://git-scm.com/doc](https://git-scm.com/doc)
	* Guía de instalación de Git: [https://git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
	* Guía de uso básico de Git: [https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
	* Crear una cuenta en GitHub: [https://github.com/join](https://github.com/join)
	* Documentación de GitHub: [https://docs.github.com/](https://docs.github.com/)
	
	Después de Aprender y entender los aspectos anteriores. Podrá proceder con los siguientes pasos:


**Paso 1:**
Cree y configure un proyecto en Python con las librerías necesarias para desarrollar el proyecto.
* Nota: para que este paso sea mas fácil, a continuación es recomendable y necesario crear dentro del proyecto un archivo .txt llamado requirements con el siguiente contenido:
``` 
fastapi  
uvicorn  
requests  
python-dotenv  
pandas
 ```
* Después se tiene que ejecutar el siguiente comando en consola para descargar todas las librerías necesarias.
``` 
pip install -r requirements.txt
 ```
Estas son todas las librerías que se van a utilizar para cumplir el objetivo.
**Paso 2:**
Después de configurar todo lo necesario en el paso anterior, cree un archivo .py llamado main en la carpeta raíz del Proyecto.
**Paso 3:**
Después del paso anterior, copie y peque el siguiente código en el archivo creado:
``` 
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
 ```
 * Nota: Si las librerías no están bien instaladas no va a funcionar el código.
 
 **Apreciaciones:**
 Para estar en este instante del experimento ya tiene que tener una base de datos creada en NocoDB, y esta tiene que tener la siguiente característica Title, Content como columnas en una tabla. Si no la tiene creada, puede seguir el siguiente tutorial:
 * En la pantalla principal oprima la Opción Create Base (puede ponerle cualquier nombre)
 * En la pantalla oprima Create New Table (puede ponerle cualquier nombre)
 * En la tabla hay un símbolo '+', oprima este botón para agregar mas columnas.
 * En el menú de búsqueda, escoja la opción "Single Line Text".
 * En Field name, escriba Content y para finalizar oprima Save Field.

**Paso 4:**
Cree un archivo .env en la carpeta raíz del proyecto. que tenga la siguiente estructura
```
API_KEY="Aqui va el apy key de la base de datos Noco DB" 
getapi=/api/v2/tables/m1dcf9vabgqnrun/records?offset=0&limit=25&where=&viewId=vwjsp4cdzqklgf3b  
postapi=https://app.nocodb.com/api/v2/tables/m1dcf9vabgqnrun/records
  ```
**Paso 5:**
Cree un repositorio en GitHub, Sincronícelo con su repositorio local y actualice los cambios en el repositorio remoto.
 ```
git init ---> Este comando es para inicializar el repositorio
git remote add origin <link del repositorio> --> para poder sincronizar el repositorio local con el remoto.
git branch -m main
  ```
**Paso 6:**
Tiene que ignorar el archivo .env para que no se suba al github y cualquier persona lo pueda ver, para hacerlo escriba el siguiente comando en consola:
 ```
git rm --cached .env
  ```

**Paso 7:**
Actualice todos los cambio realizado en github.
 ```
git add .
git commit -n "initial commit"
git push origin main
  ```
  **Creación de un Ambiente de Despliegue en Render**
 * En la pantalla principal hay una opción que dice '+ New', seleccione esa opción
* Seleccione la opción 'Web Service'
* Seleccione el proyecto que creo en github.
 * En la sección **Build Command** escriba el siguiente comando:
 ```
pip install -r requirements.txt
  ```
* En la sección **Start Command** escriba el siguiente comando:
 ```
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
  ```
  * En la sección **Environment Variables** escriba las siguiente variables:

| API_KEY | getapi | postapi |
|--|--|--|
| La Api Key de NocoDB | /api/v2/tables/m1dcf9vabgqnrun/records?offset=0&limit=25&where=&viewId=vwjsp4cdzqklgf3b | https://app.nocodb.com/api/v2/tables/m1dcf9vabgqnrun/records

* para finalizar seleccione Deploy Web Service y espere cuando ya el proyecto se haya desplegado