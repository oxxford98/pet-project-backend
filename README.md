# 🐍 Django REST API — Pet Project

Este proyecto es una API backend construida con Django y Django REST Framework, usando PostgreSQL como base de datos, ejecutada en contenedor Docker.

---

## 🚀 Requisitos previos

- Docker y Docker Compose instalados
- Python 3.11 instalado
- Git instalado

---

## 🐳 Paso 1: Levantar PostgreSQL con Docker

```bash
docker run --name postgres-pet \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_DB=pet_project \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:15
```


## 🐳 Paso 2: Crear un entorno virtual de python
# Paso 2.1: Crear entorno virtual

``` bash
python -m venv venv
```


# Paso 2.2: Activar entorno virtual
# En Linux
``` bash
source venv/bin/activate
```

# En Windows:
``` bash
./venv/Scripts/activate
```


## 🐳 Paso 3: Instalar dependencias

``` bash
pip install --upgrade pip
pip install -r requirements.txt
```


## 🐳 Paso 4: Crear archivo .env con los datos de acceso a la bd
# Debes usar los mismos datos que los usados en la generacion del contenedor de postgresql

``` bash
DB_NAME=pet_project
DB_USER=admin
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5432
```


## 🐳 Paso 5: Migrar la base de datos y crear un super usuario

``` bash
python manage.py migrate
python manage.py createsuperuser
```


## 🐳 Paso 6: Ejecutar el servidor

``` bash
python manage.py runserver
```


#### La app estará corriendo en http://127.0.0.1:8000
#### Cuando se realicen cambios en el código el servidor lo tomará sin necesidad de detenerlo.

#### Estos pasos solo se deben de ejecutar la primera vez. A partir de eso, solo se deben ejecutar los pasos 2.2 y 6 para correr el servidor

---

## 🔍 GitHub Actions - Calidad de Código

Este proyecto incluye GitHub Actions configurados para revisar automáticamente la calidad del código:

### Workflows Configurados
- **Code Quality Check**: Análisis completo con Black, isort, Flake8, Bandit y Safety
- **Basic Syntax Check**: Verificaciones básicas de sintaxis y configuración Django

### Herramientas de Desarrollo
Para instalar las herramientas de linting localmente:

```bash
pip install -r requirements-dev.txt
```

### Ejecutar Verificaciones Localmente
```bash
# Verificar formato y sintaxis
flake8 .
black --check .
isort --check-only .

# Aplicar formato automáticamente
black .
isort .

# Script de verificación completa
# En PowerShell:
.\scripts\pre-commit-check.ps1
# En Bash:
./scripts/pre-commit-check.sh
```

### Configuración
- **Flake8**: Configuración relajada en `.flake8`
- **Black**: Longitud de línea 100 caracteres
- **isort**: Compatible con Black, organización automática de imports

Ver más detalles en [`.github/README.md`](.github/README.md)
