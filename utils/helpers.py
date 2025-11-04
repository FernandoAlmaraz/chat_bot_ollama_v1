import unicodedata
import re


def _normalize_name(s: str) -> str:
    """Normaliza un nombre: minúsculas, sin acentos, sin espacios ni caracteres especiales.

    Ejemplo: 'búsqueda_propiedades' -> 'busqueda_propiedades'
    """
    if not s:
        return ""
    s = str(s).lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^\w_]", "", s)
    return s


def ejecutar_tool(tool_spec, tools):
    """Ejecuta una tool por su nombre o spec con coincidencia flexible.

    tool_spec puede ser:
      - una cadena con el nombre
      - un dict {'name': nombre, 'params': {...}}

    Devuelve el resultado de la tool o {'error': '...'} si ocurrió un error.
    """
    # Normalizar entrada
    if isinstance(tool_spec, dict):
        raw_name = tool_spec.get("name")
        params = tool_spec.get("params", {}) or {}
    else:
        raw_name = tool_spec
        params = {}

    norm_target = _normalize_name(raw_name)

    # Buscar coincidencia directa entre nombres registrados
    for tool_obj in tools:
        candidate = (
            getattr(tool_obj, "name", None) or getattr(tool_obj, "__name__", None) or ""
        )
        if _normalize_name(candidate) == norm_target:
            try:
                if hasattr(tool_obj, "invoke"):
                    return tool_obj.invoke(params or {})
                # intentar llamar como función con kwargs
                try:
                    return tool_obj(**(params or {}))
                except TypeError:
                    return tool_obj()
            except Exception as e:
                return {"error": str(e)}

    # Intentar algunos alias comunes (sin acentos / espacios)
    aliases = {
        "busqueda_propiedades": "buscar_propiedades",
        "busqueda-de-propiedades": "buscar_propiedades",
        "buscar_propiedades": "buscar_propiedades",
        "contar_propiedades": "contar_propiedades",
    }

    if norm_target in aliases:
        target_norm = _normalize_name(aliases[norm_target])
        for tool_obj in tools:
            candidate = (
                getattr(tool_obj, "name", None)
                or getattr(tool_obj, "__name__", None)
                or ""
            )
            if _normalize_name(candidate) == target_norm:
                try:
                    if hasattr(tool_obj, "invoke"):
                        return tool_obj.invoke(params or {})
                    try:
                        return tool_obj(**(params or {}))
                    except TypeError:
                        return tool_obj()
                except Exception as e:
                    return {"error": str(e)}

    # Si no encontró coincidencias, devolver None (el caller decide 500)
    return None


def detectar_tool_en_respuesta(response_text: str):
    """Detecta si la respuesta solicita usar una tool"""
    if "[USAR_TOOL:" in response_text:
        # Extraer el nombre de la tool
        start = response_text.find("[USAR_TOOL:") + len("[USAR_TOOL:")
        end = response_text.find("]", start)
        if end != -1:
            raw = response_text[start:end].strip()
            # raw puede contener nombre y parámetros, por ejemplo:
            # buscar_propiedades tipo=Casa ciudad=Cochabamba precio_max=5000
            parts = raw.split()
            if len(parts) == 0:
                return None
            name = parts[0]
            params = {}
            # parsear pares key=value
            for token in parts[1:]:
                if "=" in token:
                    k, v = token.split("=", 1)
                    # limpiar comillas si existen
                    if (v.startswith('"') and v.endswith('"')) or (
                        v.startswith("'") and v.endswith("'")
                    ):
                        v = v[1:-1]
                    # intentar convertir números
                    if re.match(r"^-?\d+$", v):
                        v_parsed = int(v)
                    else:
                        try:
                            v_parsed = float(v)
                        except Exception:
                            v_parsed = v
                    params[k] = v_parsed
                else:
                    # token suelto, podemos ignorarlo o agregar como flag True
                    params[token] = True

            return {"name": name, "params": params}
    return None
