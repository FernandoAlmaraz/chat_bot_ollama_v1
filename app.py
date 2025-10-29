from flask import Flask, request, jsonify
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

from config import Config
from tools.rekaliber_tools import obtener_info_rekaliber, obtener_info_kristof
from tools.database_tools import buscar_propiedades, contar_propiedades
from prompts.system_prompts import generar_system_prompt
from utils.helpers import ejecutar_tool, detectar_tool_en_respuesta

# ===== INICIALIZAR APP =====
app = Flask(__name__)
app.config.from_object(Config)

# ===== CONFIGURAR TOOLS =====
tools = [
    obtener_info_rekaliber,
    obtener_info_kristof,
    buscar_propiedades,
    contar_propiedades,
]

# ===== CONFIGURAR MODELO =====
print(f"🤖 Inicializando modelo: {Config.MODEL_NAME}")
llm = ChatOllama(model=Config.MODEL_NAME, temperature=Config.MODEL_TEMPERATURE)

# ===== CREAR PROMPT =====
SYSTEM_PROMPT = generar_system_prompt(tools)
prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("human", "{input}")]
)

# ===== CREAR CADENA =====
chain = prompt | llm

# ===== ENDPOINTS =====


@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint para chatear con el asistente que usa tools.

    Body JSON:
    {
        "message": "Tu pregunta aquí"
    }

    El modelo automáticamente decidirá si usar tools o no.
    """
    data = request.json

    if not data or "message" not in data:
        return jsonify({"error": 'El campo "message" es requerido'}), 400

    user_message = data["message"]

    try:
        # Primera llamada al modelo
        response = chain.invoke({"input": user_message})
        response_text = response.content

        if Config.FLASK_DEBUG:
            print(f"[DEBUG] Respuesta inicial: {response_text}")

        # Detectar si el modelo quiere usar una tool
        tool_name = detectar_tool_en_respuesta(response_text)

        if tool_name:
            if Config.FLASK_DEBUG:
                print(f"[DEBUG] Tool detectada: {tool_name}")

            # Ejecutar la tool
            tool_result = ejecutar_tool(tool_name, tools)

            if tool_result:
                # Segunda llamada con el resultado de la tool
                context_prompt = f"""Has usado la herramienta '{tool_name}' y obtuviste este resultado:

                {json.dumps(tool_result, ensure_ascii=False, indent=2)}

                Pregunta original del usuario: "{user_message}"

                Ahora responde al usuario de forma natural, clara y amigable usando esta información. 
                Incluye emojis si es apropiado. NO menciones que usaste una herramienta."""

                final_response = chain.invoke({"input": context_prompt})

                return jsonify(
                    {
                        "response": final_response.content,
                        "tool_used": tool_name,
                        "tool_result": tool_result if Config.FLASK_DEBUG else None,
                    }
                )
            else:
                return jsonify({"error": f"Tool '{tool_name}' no encontrada"}), 500

        # Si no necesitó tools, devolver la respuesta directa
        return jsonify({"response": response_text, "tool_used": None})

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/tools", methods=["GET"])
def listar_tools():
    """Lista todas las tools disponibles"""
    tools_info = []
    for tool_obj in tools:
        tools_info.append(
            {
                "nombre": tool_obj.name,
                "descripcion": tool_obj.description,
            }
        )
    return jsonify({"tools": tools_info})


@app.route("/health", methods=["GET"])
def health():
    """Verifica el estado del servicio"""
    return jsonify(
        {
            "status": "ok",
            "modelo": Config.MODEL_NAME,
            "tools_disponibles": len(tools),
            "version": "1.0.0",
        }
    )


# ===== EJECUTAR APP =====
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Chat Bot con Ollama - Rekaliber")
    print("=" * 50)
    print(f"📍 Host: {Config.FLASK_HOST}")
    print(f"🔌 Puerto: {Config.FLASK_PORT}")
    print(f"🤖 Modelo: {Config.MODEL_NAME}")
    print(f"🔧 Tools disponibles: {len(tools)}")
    print("=" * 50)

    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
