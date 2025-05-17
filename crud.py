from sqlalchemy.orm import Session, selectinload
from models import Usuario, Producto, Cesta
import schemas

# ------------------
# Operaciones Usuario
# ------------------

def get_usuario(db: Session, usuario_id: int) -> Usuario | None:
    return (
        db.query(Usuario)
        .options(
            selectinload(Usuario.cestas)
              .selectinload(Cesta.productos)
        )
        .filter(Usuario.id == usuario_id)
        .first()
    )

def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    return (
        db.query(Usuario)
        .options(
            selectinload(Usuario.cestas)
              .selectinload(Cesta.productos)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

async def create_usuario(db: Session, usuario: schemas.UsuarioCreate) -> Usuario:
    db_usuario = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        ciudad=usuario.ciudad
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# ------------------
# Operaciones Producto
# ------------------

def get_producto(db: Session, producto_id: int) -> Producto | None:
    return db.query(Producto).get(producto_id)

async def create_producto(db: Session, producto: schemas.ProductoCreate) -> Producto:
    db_producto = Producto(
        nombre=producto.nombre,
        precio=producto.precio
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# ------------------
# Operaciones Cesta
# ------------------

def get_cesta(db: Session, cesta_id: int) -> Cesta | None:
    return (
        db.query(Cesta)
        .options(
            selectinload(Cesta.productos),
            selectinload(Cesta.usuario)
        )
        .get(cesta_id)
    )

async def create_cesta(db: Session, cesta: schemas.CestaCreate, usuario_id: int) -> Cesta:
    db_cesta = Cesta(usuario_id=usuario_id)
    db.add(db_cesta)
    db.commit()
    db.refresh(db_cesta)
    if cesta.productos:
        for prod_id in cesta.productos:
            producto = get_producto(db, prod_id)
            if producto:
                db_cesta.productos.append(producto)
        db.commit()
        db.refresh(db_cesta)
    return db_cesta

def get_cestas_usuario(db: Session, usuario_id: int) -> list[Cesta]:
    return db.query(Cesta).filter(Cesta.usuario_id == usuario_id).all()

def agregar_producto_a_cesta(db: Session, cesta_id: int, producto_id: int) -> Cesta | None:
    db_cesta = get_cesta(db, cesta_id)
    producto = get_producto(db, producto_id)
    if db_cesta and producto and producto not in db_cesta.productos:
        db_cesta.productos.append(producto)
        db.commit()
        db.refresh(db_cesta)
        return db_cesta
    return None

def eliminar_producto_de_cesta(db: Session, cesta_id: int, producto_id: int) -> Cesta | None:
    db_cesta = get_cesta(db, cesta_id)
    producto = get_producto(db, producto_id)
    if db_cesta and producto and producto in db_cesta.productos:
        db_cesta.productos.remove(producto)
        db.commit()
        db.refresh(db_cesta)
        return db_cesta
    return None