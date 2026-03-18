#importaciones
from fastapi import FastAPI 
from app.routers import usuarios, misc


#Inicializacion o Instacia de la API
app= FastAPI(
    title= 'Mi primer API',
    description='Diego Rivera Diaz',
    version='1,0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)





    
