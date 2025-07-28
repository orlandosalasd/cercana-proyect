# DECISION LOG

## [1] Base de datos: PostgreSQL

### Contexto
Se requiere base de datos realcion robusta que tenga buen soporte con FastAPi y Alembic.

### Decisión
Se elige PostgreSQL como sistema gestor de base de datos.

### Razonamiento
Buen soporte en herramientas como SQLAlchemy y Alembic.

## [2] ORM: SQLAlchemy 

### Contexto
Se requeria una capa de acceso a la base de datos robusca, flexible y compatible con PostgreSQL.

### Decisión
Se eligió SQLAlchemy como ORM principal para interactuar con la base de datos.

### Razonamiento
Excelente compatibilidad con PostgreSQL, que es el motor usado en este proyecto.


## [3] Migraciones: Alembic 

### Contexto
Se necesita una herramienta para mantener un control de versiones del esquema de base de datos.

### Decisión
Se elige Alembic como sistema de migración de base de datos.

### Razonamiento
Es la herramienta oficial de migración para SQLAlchemy.
