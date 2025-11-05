#!/bin/bash
# Script de pre-commit opcional para ejecutar verificaciones locales

echo "🔍 Ejecutando verificaciones de código..."

# Verificar sintaxis Python
echo "📝 Verificando sintaxis Python..."
python -m py_compile $(find . -name "*.py" -not -path "./migrations/*" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./__pycache__/*") || {
    echo "❌ Error de sintaxis encontrado"
    exit 1
}

# Verificar con flake8
echo "🔎 Ejecutando Flake8..."
flake8 . --config=.flake8 || {
    echo "⚠️  Advertencias de Flake8 encontradas"
    echo "💡 Puedes continuar o ejecutar: flake8 . --config=.flake8"
}

# Verificar formato con black
echo "🎨 Verificando formato con Black..."
black --check --diff . || {
    echo "⚠️  Formato de código no estándar"
    echo "💡 Ejecuta: black . para aplicar formato automáticamente"
}

# Verificar imports con isort
echo "📦 Verificando imports con isort..."
isort --check-only --diff . || {
    echo "⚠️  Imports no ordenados correctamente"
    echo "💡 Ejecuta: isort . para ordenar automáticamente"
}

echo "✅ Verificaciones completadas"
echo ""
echo "💡 Para aplicar formato automáticamente:"
echo "   black ."
echo "   isort ."