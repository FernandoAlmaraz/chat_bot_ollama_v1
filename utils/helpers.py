def ejecutar_tool(tool_name: str, tools):
    """Ejecuta una tool por su nombre"""
    for tool_obj in tools:
        if tool_obj.name == tool_name:
            return tool_obj.invoke({})
    return None


def detectar_tool_en_respuesta(response_text: str):
    """Detecta si la respuesta solicita usar una tool"""
    if "[USAR_TOOL:" in response_text:
        # Extraer el nombre de la tool
        start = response_text.find("[USAR_TOOL:") + len("[USAR_TOOL:")
        end = response_text.find("]", start)
        if end != -1:
            tool_name = response_text[start:end].strip()
            return tool_name
    return None
