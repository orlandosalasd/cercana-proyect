# Crehana Proyect

Proyecto backend construido con **FastAPI**, **SQLAlchemy**, **Alembic** y base de datos **PostgreSQL**. El entorno de desarrollo y despliegue se gestiona con **Docker** y **Docker Compose**.


## Tecnologías utilizadas

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x (async)
- Alembic
- Pydantic v2
- Docker & Docker Compose
- Poetry (gestor de dependencias)
- Uvicorn

## Requisitos

- Docker
- Docker Compose

## Cómo levantar el proyecto con Docker

### 1. Clona el repositorio

```bash
git clone https://github.com/orlandosalasd/cercana-proyect.git
cd crehana-proyect
```

### 2. Es importante darle permisos a este archivo .sh para que levante las migraciones al momento de levantar Docker
```bash
chmod +x entrypoint.sh
```

### 3. Crear/Configurar .env
Te puedes guiar del archivo .evn.example

### 4. Levanta los servicios
```bash
docker-compose up --build
```
Una vez levantado los servicios puedes acceder a http://localhost:8000

### 5. Puedes acceder a la documentacion automatica
http://localhost:8000/docs


## Cómo Ejecutar los Tests.

Se configuro un archivo docker-compose.test.yml para levantar una base de datos de pruebas.

### 1. Levantamos el servicio
```bash
docker-compose -f docker-compose.test.yml up -d
```

### 2. Ejecutamos Pytest
```bash
pytest
```
ya con la configuracion de pytest.ini podemos ver el coverage.

### 3. Bajamos los servicos y eliminamos volumenes.
```bash
docker-compose -f docker-compose.test.yml down -v
```
