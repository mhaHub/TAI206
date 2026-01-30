#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#Inicializacion o Instacia de la API
app= FastAPI(
    title= 'Mi primer API',
    description='Diego Rivera Diaz',
    version='1,0'
)

#BD Ficticia
usuarios=[
    {"id":1,"Nombre":"Frosty","Edad":21},
    {"id":2,"Nombre":"Jack","Edad":15},
    {"id":3,"Nombre":"Rubio","Edad":28},
]


#Endpoints
@app.get("/",tags=['Inicio'])
async def comoandamosrasa():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienveidos a tu API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje":"Tu calificacion en TAI es 10 "}

@app.get("/v1/usuarios/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return { "usuario encontrado":id }


@app.get("/v1/usuarios_op/", tags=['Parametro Opcional'])
async def consultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id,"Datos": usuario }
        return { "Mensaje":"Usuario no encontrado" }
    else:
        return { "Aviso":"No se proporciono ID" }

