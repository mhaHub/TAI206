from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags=['Varios'])

#Endpoints
@router.get("/")
async def comoandamosrasa():
    return {"mensaje":"Hola mundo FastAPI"}   

@router.get("/v1/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienveidos a tu API REST"}

@router.get("/v1/calificaciones")
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje":"Tu calificacion en TAI es 10 "}

@router.get("/v1/parametroo/{id}")
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return { "usuario encontrado":id }


@router.get("/v1/ParametroOp/")
async def consultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id,"Datos": usuario }
        return { "Mensaje":"Usuario no encontrado" }
    else:
        return { "Aviso":"No se proporciono ID" }
