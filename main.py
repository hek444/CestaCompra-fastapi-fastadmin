import os
from dotenv import load_dotenv
load_dotenv()

from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from database_async import engine, Base, async_sessionmaker, get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastadmin import fastapi_app as admin_app, register, SqlAlchemyModelAdmin
from models import Usuario, Producto, Cesta
import schemas, crud

app = FastAPI()

# Startup: crea tablas en el engine async y siembra admin
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker() as session:
        existing = await session.get(Usuario, 1)
        if not existing:
            admin_user = os.getenv("ADMIN_USER", "admin")
            session.add(Usuario(id=1, nombre=admin_user, apellido="", ciudad=""))
            await session.commit()

# FastAdmin
@register(Usuario, sqlalchemy_sessionmaker=async_sessionmaker)
class UsuarioAdmin(SqlAlchemyModelAdmin):
    list_display = ("id", "nombre", "apellido", "ciudad")
    list_display_links = ("id", "nombre")
    list_filter = ("ciudad",)
    search_fields = ("nombre", "apellido")

    async def authenticate(self, username: str, password: str) -> int | None:
        if username == os.getenv("ADMIN_USER") and password == os.getenv("ADMIN_PASSWORD"):
            return 1
        return None

@register(Producto, sqlalchemy_sessionmaker=async_sessionmaker)
class ProductoAdmin(SqlAlchemyModelAdmin):
    exclude = ("cestas",)
    list_display = ("id", "nombre", "precio")
    list_filter = ("precio",)
    search_fields = ("nombre",)

@register(Cesta, sqlalchemy_sessionmaker=async_sessionmaker)
class CestaAdmin(SqlAlchemyModelAdmin):
    list_display = ("id", "usuario", "productos")
    list_filter = ("usuario",)
    form_columns = ("usuario", "productos")
    filter_horizontal = ("productos",)

app.mount("/admin", admin_app)

# Dependencia sync para los endpoints REST

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas Usuarios sync
@app.post("/usuarios/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db, usuario)

@app.get("/usuarios/", response_model=List[schemas.Usuario])
def leer_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_usuarios(db, skip, limit)

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/{usuario_id}/cestas", response_model=List[schemas.Cesta])
def leer_cestas_de_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud.get_cestas_usuario(db, usuario_id)

# Rutas Productos sync
@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db, producto)

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def leer_producto(producto_id: int, db: Session = Depends(get_db)):
    prod = crud.get_producto(db, producto_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod

# Rutas Cestas sync
@app.post("/usuarios/{usuario_id}/cestas/", response_model=schemas.Cesta)
def crear_cesta_para_usuario(usuario_id: int, cesta: schemas.CestaCreate, db: Session = Depends(get_db)):
    return crud.create_cesta(db, cesta, usuario_id)

@app.get("/cestas/{cesta_id}", response_model=schemas.Cesta)
def leer_cesta(cesta_id: int, db: Session = Depends(get_db)):
    cesta = crud.get_cesta(db, cesta_id)
    if not cesta:
        raise HTTPException(status_code=404, detail="Cesta no encontrada")
    return cesta

@app.post("/cestas/{cesta_id}/productos/{producto_id}", response_model=schemas.Cesta)
def agregar_producto(cesta_id: int, producto_id: int, db: Session = Depends(get_db)):
    result = crud.agregar_producto_a_cesta(db, cesta_id, producto_id)
    if not result:
        raise HTTPException(status_code=404, detail="Cesta o producto no encontrado")
    return result

@app.delete("/cestas/{cesta_id}/productos/{producto_id}", response_model=schemas.Cesta)
def eliminar_producto(cesta_id: int, producto_id: int, db: Session = Depends(get_db)):
    result = crud.eliminar_producto_de_cesta(db, cesta_id, producto_id)
    if not result:
        raise HTTPException(status_code=404, detail="Cesta o producto no encontrado")
    return result