from fastapi import status, HTTPException, Depends, APIRouter
from app.moldels.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router = APIRouter(
    prefix= "/v1/usuarios",
    tags= ['CRUD HTTP']
    )

#Endpoints CRUD usuarios
@router.get("/")
async def consultaUsuarios(db:Session = Depends(get_db)):
    
    consulta_usuarios= db.query(usuarioDB).all()
    
    return{
        "status":"200",
        "total": len(consulta_usuarios),
        "usuarios":consulta_usuarios
    }
    
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuario:UsuarioBase, db:Session = Depends(get_db)):
    
    nuevoUsuario= usuarioDB(nombre= usuario.nombre, edad= usuario.edad)
    
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    
    return{
        "Mensaje": "Usuario agregado",
        "datos":usuario,
        "status":"200"
    }


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuarios(id: int, usuario_actualizado: UsuarioBase, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario.nombre = usuario_actualizado.nombre
    usuario.edad = usuario_actualizado.edad

    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "Usuario actualizado correctamente",
        "datos": usuario
    }

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_Peticion), db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="El Usuario no existe"
        )

    db.delete(usuario)
    db.commit()

    return {
        "message": f"Usuario eliminado correctamente por {usuarioAuth}"
    }
