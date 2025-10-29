#!/bin/bash

echo "🚀 Iniciando Chat Bot..."

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta primero: ./setup.sh"
    exit 1
fi

# Activar entorno virtual de forma más robusta
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ No se puede activar el entorno virtual"
    exit 1
fi

# Verificar que Flask está instalado
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Flask no está instalado. Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar si Ollama está corriendo
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama no está corriendo. Iniciando Ollama..."
    ollama serve &
    sleep 3
fi

# Ejecutar la aplicación
echo "✅ Iniciando Flask..."
python app.py