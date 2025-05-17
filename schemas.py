from pydantic import BaseModel
from typing import List

class ProductoBase(BaseModel):
    nombre: str
    precio: float

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}

class CestaBase(BaseModel):
    usuario_id: int
    productos: List[int] = []

class CestaCreate(CestaBase):
    pass

class Cesta(CestaBase):
    id: int
    productos: List[Producto] = []

    class Config:
        model_config = {"from_attributes": True}

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    ciudad: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    cestas: List[Cesta] = []

    class Config:
        model_config = {"from_attributes": True}