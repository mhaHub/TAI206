from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import status, HTTPException, Depends

#Seguridad con HTTP Basic
security = HTTPBasic()

def verificar_Peticion(credentials:HTTPBasicCredentials=Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username,"martingd")
    contraAuth = secrets.compare_digest(credentials.password,"1234")
    
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no validas"
        )
        
    return credentials.username