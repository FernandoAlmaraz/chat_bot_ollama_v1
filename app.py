from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

from config import Config
import traceback
from tools.rekaliber_tools import obtener_info_rekaliber, obtener_info_kristof
from tools.database_tools import buscar_propiedades, contar_propiedades
from prompts.system_prompts import generar_system_prompt
from utils.helpers import ejecutar_tool, detectar_tool_en_respuesta

# ===== INICIALIZAR APP =====
app = Flask(__name__)
app.config.from_object(Config)

# ===== CONFIGURAR CORS =====
CORS(app, resources={r"/*": {"origins": "*"}})

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
        print(f"[REQUEST] user_message={user_message}")
        response = chain.invoke({"input": user_message})
        response_text = getattr(response, "content", None)

        if response_text is None:
            raise RuntimeError("Respuesta del modelo vacía o inválida")

        if Config.FLASK_DEBUG:
            print(f"[DEBUG] Respuesta inicial: {response_text}")

        # Detectar si el modelo quiere usar una tool (puede venir con params)
        tool_spec = detectar_tool_en_respuesta(response_text)

        if tool_spec:
            tool_name = (
                tool_spec.get("name") if isinstance(tool_spec, dict) else str(tool_spec)
            )
            if Config.FLASK_DEBUG:
                print(
                    f"[DEBUG] Tool detectada: {tool_name} params={tool_spec.get('params') if isinstance(tool_spec, dict) else {}}"
                )

            # Ejecutar la tool (ejecutar_tool acepta ahora spec o nombre simple)
            tool_result = ejecutar_tool(tool_spec, tools)

            # Verificar resultado de la tool
            if isinstance(tool_result, dict) and tool_result.get("error"):
                # La tool devolvió un error internamente
                err = tool_result.get("error")
                print(f"[ERROR] tool '{tool_name}' returned error: {err}")
                return (
                    jsonify({"error": f"Tool '{tool_name}' error: {err}"}),
                    500,
                )

            if tool_result:
                # Segunda llamada con el resultado de la tool
                context_prompt = f"""Has usado la herramienta '{tool_name}' y obtuviste este resultado:

                {json.dumps(tool_result, ensure_ascii=False, indent=2)}

                Pregunta original del usuario: "{user_message}"

                Ahora responde al usuario de forma natural, clara y amigable usando esta información. 
                Incluye emojis si es apropiado. NO menciones que usaste una herramienta."""

                final_response = chain.invoke({"input": context_prompt})

                final_text = getattr(final_response, "content", None)
                if final_text is None:
                    raise RuntimeError("Respuesta final del modelo vacía o inválida")

                return jsonify(
                    {
                        "response": final_text,
                        "tool_used": tool_name,
                        "tool_result": tool_result if Config.FLASK_DEBUG else None,
                    }
                )
            else:
                return jsonify({"error": f"Tool '{tool_name}' no encontrada"}), 500

        # Si no necesitó tools, devolver la respuesta directa
        return jsonify({"response": response_text, "tool_used": None})

    except Exception as e:
        tb = traceback.format_exc()
        print(f"[ERROR] {str(e)}")
        print(tb)
        if Config.FLASK_DEBUG:
            return jsonify({"error": str(e), "trace": tb}), 500
        return jsonify({"error": "Internal server error"}), 500


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


@app.route("/debug/db", methods=["GET"])
def debug_db():
    """Endpoint de ayuda para testear la conexión a la base de datos y buscar propiedades."""
    ciudad = request.args.get("ciudad")
    try:
        resultados = buscar_propiedades(ciudad=ciudad)
        return jsonify({"ok": True, "result": resultados})
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return jsonify({"ok": False, "error": str(e), "trace": tb}), 500


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
