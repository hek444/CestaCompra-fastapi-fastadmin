from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database_async import Base

cestas_productos = Table(
    "cestas_productos", Base.metadata,
    Column("cesta_id", Integer, ForeignKey("cestas.id"), primary_key=True),
    Column("producto_id", Integer, ForeignKey("productos.id"), primary_key=True),
)

class Usuario(Base):
    __tablename__ = "usuarios"
    id       = Column(Integer, primary_key=True, index=True)
    nombre   = Column(String(255))
    apellido = Column(String(255))
    ciudad   = Column(String(255))
    cestas   = relationship("Cesta", back_populates="usuario")

    def __str__(self):
        return self.nombre  

class Producto(Base):
    __tablename__ = "productos"
    id      = Column(Integer, primary_key=True, index=True)
    nombre  = Column(String(255), index=True)
    precio  = Column(Float)
    cestas  = relationship("Cesta", secondary=cestas_productos, back_populates="productos")

    def __str__(self):
        return self.nombre  

class Cesta(Base):
    __tablename__ = "cestas"
    id         = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario    = relationship("Usuario", back_populates="cestas")
    productos  = relationship("Producto", secondary=cestas_productos, back_populates="cestas")
