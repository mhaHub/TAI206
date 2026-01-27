#importaciones
from fastapi import FastAPI

#Inicializacion
app= FastAPI()

#Endpoints
@app.get("/")
async def comoandamosrasa():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienveidos a tu API REST"}
