#importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

#Inicializacion o Instacia de la API
app= FastAPI(
    title= 'Mi primer API',
    description='Diego Rivera Diaz',
    version='1,0'
)

#BD Ficticia
usuarios=[
    {"id":1,"nombre":"frosty","edad":21},
    {"id":2,"nombre":"jack","edad":15},
    {"id":3,"nombre":"rubio","edad":28},
]


#Modelo de Validacion Pydantic
class UsuarioBase(BaseModel):
    id: int = Field(...,gt=0,description="Identificador de Usuario", example="1" )
    nombre: str = Field(...,min_length=3,max_length=50,description="Nombre del usuario")
    edad: int = Field(...,ge=0,le=121,description="Edad valida entre 0 y 121")

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

@app.get("/v1/parametroo/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return { "usuario encontrado":id }


@app.get("/v1/ParametroOp/", tags=['Parametro Opcional'])
async def consultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id,"Datos": usuario }
        return { "Mensaje":"Usuario no encontrado" }
    else:
        return { "Aviso":"No se proporciono ID" }

    
@app.get("/v1/usuarios/", tags=['CRUD Usuarios'])
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
@app.get("/v1/usuarios/{id}")
async def obtener_usuario(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            return usuario

    raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@app.post("/v1/usuarios/", tags=['CRUD Usuarios'])
async def agregar_usuarios(usuario:UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail= "El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "Mensaje": "Usuario agregado",
        "datos":usuario,
        "status":"200"
    }


@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuarios(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": usuario_actualizado
            }
    
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "datos": usr
            }
    
    raise HTTPException(
        status_code=404,
        detail="El Usuario no existe"
    )
