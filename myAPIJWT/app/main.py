#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

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

#Configuracion JWT
CLAVE_PRIVADA = "mi_clave_secreta"
TIPO_ALGORITMO = "HS256"
TIEMPO_EXPIRACION = 30


#Modelo de Validacion Pydantic
class UsuarioBase(BaseModel):
    id: int = Field(...,gt=0,description="Identificador de Usuario", example="1" )
    nombre: str = Field(...,min_length=3,max_length=50,description="Nombre del usuario")
    edad: int = Field(...,ge=0,le=121,description="Edad valida entre 0 y 121")

#Configuracion OAuth2 y funcion
esquema_oauth = OAuth2PasswordBearer(tokenUrl="token")

def crear_token_acceso(datos: dict):
    datos_copia = datos.copy()
    tiempo_limite = datetime.now(timezone.utc) + timedelta(minutes=TIEMPO_EXPIRACION)
    datos_copia.update({"exp": tiempo_limite})
    token_generado = jwt.encode(datos_copia, CLAVE_PRIVADA, algorithm=TIPO_ALGORITMO)
    return token_generado

#Funcion para validar el token
async def validar_token(token: str = Depends(esquema_oauth)):
    try:
        datos_decodificados = jwt.decode(token, CLAVE_PRIVADA, algorithms=[TIPO_ALGORITMO])
        nombre_usuario = datos_decodificados.get("sub")

        if nombre_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return nombre_usuario

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


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
async def actualizar_usuarios( id: int, usuario_actualizado: dict, usuario_actual: str = Depends(validar_token)):
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
async def eliminar_usuario(
    id: int,
    usuario_actual: str = Depends(validar_token)
):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "realizado_por": usuario_actual
            }

    raise HTTPException(
        status_code=404,
        detail="El usuario no existe"
    )


#Nuevo endpoint para usar la autenticacion
@app.post("/token")
async def iniciar_sesion(datos_formulario: OAuth2PasswordRequestForm = Depends()):
    
    if datos_formulario.username != "martingd" or datos_formulario.password != "1234":
        raise HTTPException(
            status_code=400,
            detail="Credenciales incorrectas"
        )

    token = crear_token_acceso({"sub": datos_formulario.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
