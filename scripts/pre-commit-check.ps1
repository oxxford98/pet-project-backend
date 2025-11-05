# Script de pre-commit para Windows PowerShell
# Ejecutar verificaciones de código antes de commit

Write-Host "🔍 Ejecutando verificaciones de código..." -ForegroundColor Cyan

# Verificar sintaxis Python
Write-Host "📝 Verificando sintaxis Python..." -ForegroundColor Yellow
$pythonFiles = Get-ChildItem -Recurse -Filter "*.py" | Where-Object {
    $_.FullName -notmatch "migrations" -and
    $_.FullName -notmatch "\.venv" -and
    $_.FullName -notmatch "venv" -and
    $_.FullName -notmatch "__pycache__"
}

foreach ($file in $pythonFiles) {
    python -m py_compile $file.FullName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error de sintaxis en: $($file.FullName)" -ForegroundColor Red
        exit 1
    }
}

# Verificar con flake8
Write-Host "🔎 Ejecutando Flake8..." -ForegroundColor Yellow
flake8 . --config=.flake8
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Advertencias de Flake8 encontradas" -ForegroundColor Yellow
    Write-Host "💡 Puedes continuar o ejecutar: flake8 . --config=.flake8" -ForegroundColor Cyan
}

# Verificar formato con black
Write-Host "🎨 Verificando formato con Black..." -ForegroundColor Yellow
black --check --diff .
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Formato de código no estándar" -ForegroundColor Yellow
    Write-Host "💡 Ejecuta: black . para aplicar formato automáticamente" -ForegroundColor Cyan
}

# Verificar imports con isort
Write-Host "📦 Verificando imports con isort..." -ForegroundColor Yellow
isort --check-only --diff .
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Imports no ordenados correctamente" -ForegroundColor Yellow
    Write-Host "💡 Ejecuta: isort . para ordenar automáticamente" -ForegroundColor Cyan
}

Write-Host "✅ Verificaciones completadas" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Para aplicar formato automáticamente:" -ForegroundColor Cyan
Write-Host "   black ." -ForegroundColor White
Write-Host "   isort ." -ForegroundColor White