# API de Gestión de Compras con FastAPI y SQLAlchemy

Este proyecto es una API RESTful construida con el framework FastAPI de Python y utiliza SQLAlchemy como ORM para interactuar con una base de datos MySQL. Permite gestionar usuarios, productos y cestas de la compra con relaciones entre ellos. Además, incluye un panel de administración generado con `fastapi-admin` para facilitar la gestión de los datos.

## Prerrequisitos

Asegúrate de tener instalado lo siguiente en tu sistema:

* **Python 3.8+**
* **pip** (el gestor de paquetes de Python)

## Configuración de Variables de Entorno

La API utiliza variables de entorno para configurar la conexión a la base de datos. Debes crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

DATABASE_URL="mysql+mysqldb://&lt;usuario>:&lt;contraseña>@&lt;servidor>/&lt;basededatos>"

Reemplaza los marcadores de posición `<usuario>`, `<contraseña>`, `<servidor>` y `<basededatos>` con las credenciales de tu base de datos MySQL. Por ejemplo:

DATABASE_URL="mysql+mysqldb://root:mypassword@localhost/compra_db"

**Nota:** Asegúrate de que la base de datos especificada exista en tu servidor MySQL.

## Instalación

1.  **Clona el repositorio (si lo tienes en uno):**

    ```bash
    git clone <tu_repositorio>
    cd compra_api
    ```

2.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

    Si no tienes un archivo `requirements.txt`, puedes crearlo con las dependencias que hemos instalado:

    ```bash
    pip freeze > requirements.txt
    ```

    O instalar las dependencias directamente:

    ```bash
    pip install fastapi uvicorn sqlalchemy mysqlclient fastapi-admin Jinja2 python-dotenv
    ```

    **Nota:** Hemos añadido `python-dotenv` para cargar las variables de entorno desde el archivo `.env`. Asegúrate de importarlo y cargarlo en tu `main.py` si aún no lo haces. Por ejemplo, al principio de `main.py`:

    ```python
    from dotenv import load_dotenv
    load_dotenv()
    from core.config import settings # Si tienes un archivo de configuración
    if not settings.DATABASE_URL: # Si no usas un archivo de configuración
        import os
        settings.DATABASE_URL = os.environ.get("DATABASE_URL")
    ```

## Cómo Arrancar el Proyecto

1.  **Asegúrate de que tu entorno virtual esté activado.**

2.  **Ejecuta el servidor Uvicorn:**

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

    * `main`: Es el nombre del archivo Python principal de tu API (donde se encuentra la instancia de FastAPI).
    * `app`: Es el nombre de la instancia de FastAPI dentro de `main.py`.
    * `--reload`: Activa la recarga automática del servidor al detectar cambios en el código (útil para desarrollo).
    * `--host 0.0.0.0`: Permite que la API sea accesible desde cualquier dirección IP de tu sistema.
    * `--port 8000`: Especifica el puerto en el que la API escuchará (puedes cambiarlo si lo deseas).

## Acceder a la API

Una vez que el servidor Uvicorn esté en funcionamiento, puedes acceder a la API en las siguientes URLs:

* **Documentación interactiva (Swagger UI):** `http://localhost:8000/docs`
* **Documentación alternativa (Redoc):** `http://localhost:8000/redoc`
* **Panel de Administración:** `http://localhost:8000/admin` (requerirá la implementación de la autenticación).

## Modelos de la Base de Datos

* **Usuarios:** `nombre`, `apellido`, `ciudad`
* **Productos:** `nombre`, `precio`
* **Cestas:** Relacionado con `Usuarios` y `Productos` (muchos a muchos).

## Endpoints de la API (Ejemplos)

* `POST /usuarios/`: Crear un nuevo usuario.
* `GET /usuarios/`: Listar usuarios.
* `GET /usuarios/{usuario_id}`: Obtener un usuario por ID.
* `POST /productos/`: Crear un nuevo producto.
* `GET /productos/{producto_id}`: Obtener un producto por ID.
* `POST /usuarios/{usuario_id}/cestas/`: Crear una nueva cesta para un usuario.
* `GET /cestas/{cesta_id}`: Obtener una cesta por ID.
* `POST /cestas/{cesta_id}/productos/{producto_id}`: Agregar un producto a una cesta.
* `DELETE /cestas/{cesta_id}/productos/{producto_id}`: Eliminar un producto de una cesta.