# GitHub Actions - Revisión de Código

Este proyecto incluye GitHub Actions configurados para revisar automáticamente la calidad del código Python.

## Workflows Configurados

### 1. Code Quality Check (`code_quality.yml`)
Ejecuta una revisión completa de calidad de código que incluye:

- **Black**: Verificación de formato de código
- **isort**: Verificación de ordenamiento de imports
- **Flake8**: Análisis de sintaxis y estilo (configuración relajada)
- **Bandit**: Análisis de seguridad básico
- **Safety**: Verificación de vulnerabilidades en dependencias

### 2. Basic Syntax Check (`syntax_check.yml`)
Ejecuta verificaciones básicas:

- Compilación de sintaxis Python
- Django system checks
- Verificación de estructura de imports

## Configuración Relajada

Los linters están configurados con reglas no muy estrictas:

### Flake8 (`.flake8`)
- Longitud máxima de línea: 100 caracteres
- Complejidad máxima: 15
- Ignora errores comunes como E203, W503, E501, F401
- Excluye migraciones, static files, y archivos de configuración

### Black (`pyproject.toml`)
- Longitud de línea: 100 caracteres
- Compatible con Python 3.9, 3.10, 3.11
- Excluye migraciones y archivos estáticos

### isort (`pyproject.toml`)
- Perfil compatible con Black
- Organización automática de imports
- Reconoce módulos de Django y first-party

## Ejecución

Los workflows se ejecutan automáticamente en:
- Push a ramas `main` o `develop`
- Pull requests hacia `main` o `develop`

## Ejecución Local

Para ejecutar las mismas verificaciones localmente:

```bash
# Instalar herramientas
pip install flake8 black isort bandit safety

# Verificar formato
black --check .

# Verificar imports
isort --check-only .

# Verificar sintaxis y estilo
flake8 .

# Verificar seguridad
bandit -r . -ll -x "*/tests/*,*/migrations/*"

# Verificar dependencias
safety check
```

## Aplicar Formato Automáticamente

Para aplicar formato automáticamente:

```bash
# Formatear código
black .

# Ordenar imports
isort .
```