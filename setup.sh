#!/bin/bash

echo "🚀 Configurando Chat Bot con Ollama..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Verificar si Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama no está instalado."
    echo "Instálalo desde: https://ollama.ai"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Verificar si el modelo está descargado
echo "🤖 Verificando modelo Ollama..."
if ! ollama list | grep -q "llama3.2:latest"; then
    echo "📥 Descargando modelo llama3.2..."
    ollama pull llama3.2:latest
fi

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
fi

echo "✅ ¡Configuración completada!"
echo ""
echo "Para ejecutar la aplicación:"
echo "  ./run.sh"
echo ""
echo "O manualmente:"
echo "  source venv/bin/activate"
echo "  python app.py"