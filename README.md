# Chat Bot con Ollama - Rekaliber

Bot conversacional inteligente con soporte para herramientas (tools) usando Ollama y LangChain.

## 🚀 Características

- ✅ Integración con Ollama (llama3.2)
- ✅ Sistema de tools personalizable
- ✅ Información sobre Rekaliber y su fundador
- ✅ Búsqueda de propiedades en base de datos SQLite
- ✅ Historial de conversaciones persistente
- ✅ Respuestas contextuales y amigables
- ✅ Arquitectura modular y escalable
- ✅ Interfaz web con ASTRO

## 📋 Requisitos

- Python 3.12+
- Ollama instalado y corriendo
- Modelo llama3.2:latest descargado

## 🛠️ Instalación

### Opción 1: Instalación automática (Linux/Mac)
```bash
chmod +x setup.sh
./setup.sh
```

### Opción 2: Instalación manual
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelo Ollama
ollama pull llama3.2:latest

# Crear archivo .env
cp .env.example .env
```

## ▶️ Ejecución

### Opción 1: Script automático (Linux/Mac)
```bash
chmod +x run.sh
./run.sh
```

### Opción 2: Ejecución manual
```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar Ollama (si no está corriendo)
ollama serve &

# Ejecutar aplicación
python app.py
```

## 📡 Endpoints

### POST /chat
Enviar mensaje al chatbot
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué es Rekaliber?"}'
```

### GET /tools
Listar herramientas disponibles
```bash
curl http://localhost:5000/tools
```

### GET /health
Verificar estado del servicio
```bash
curl http://localhost:5000/health
```
🖥️ Frontend – Proyecto Astro (Chat_UI)

El frontend vive en la carpeta Chat_UI. Es un proyecto Astro con componentes React.

✅ Instalación
cd Chat_UI
npm install

✅ Modo desarrollo
npm run dev


El servidor de Astro se abrirá normalmente en:

http://localhost:4321

✅ Comunicación con tu API

Crea un archivo .env dentro de Chat_UI:

PUBLIC_API_URL="http://localhost:5000/chat"

## 🔧 Estructura del Proyecto
```
chat_bot_basic/
├── app.py                    # Aplicación principal
├── config.py                 # Configuraciones
├── requirements.txt          # Dependencias
├── setup.sh                  # Script de instalación
├── run.sh                    # Script de ejecución
├── tools/                    # Herramientas del bot
│   ├── rekaliber_tools.py
│   └── database_tools.py
├── prompts/                  # System prompts
│   └── system_prompts.py
└── utils/                    # Utilidades
    └── helpers.py
```

## 🎯 Agregar Nuevas Tools

1. Crear nueva tool en `tools/`:
```python
from langchain_core.tools import tool

@tool
def mi_nueva_tool() -> dict:
    """Descripción de la tool"""
    return {"dato": "valor"}
```

2. Importarla en `app.py`:
```python
from tools.mi_archivo import mi_nueva_tool

tools = [
    obtener_info_rekaliber,
    obtener_info_kristof,
    mi_nueva_tool  # Agregar aquí
]
```

## 📝 Configuración

Edita el archivo `.env` para personalizar:
```bash
MODEL_NAME=llama3.2:latest
MODEL_TEMPERATURE=0.7
FLASK_PORT=5000
FLASK_DEBUG=True
```

## 🐛 Troubleshooting

**Error: Ollama no encontrado**
```bash
# Instalar Ollama
curl https://ollama.ai/install.sh | sh
```

**Error: Modelo no encontrado**
```bash
ollama pull llama3.2:latest
```

**Error: Puerto en uso**
```bash
# Cambiar puerto en .env
FLASK_PORT=8000
```

## 📄 Licencia

MIT License - Rekaliber 2025 
BY : FERCHEX 👹