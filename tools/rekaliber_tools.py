from langchain_core.tools import tool


@tool
def obtener_info_rekaliber() -> dict:
    """
    Obtiene información completa sobre la empresa Rekaliber.

    Usa esta herramienta cuando el usuario pregunte sobre:
    - Qué es Rekaliber
    - La empresa Rekaliber
    - Información de la compañía
    - Quién fundó Rekaliber

    Returns:
        dict: Información detallada de la empresa
    """
    return {
        "empresa": "Rekaliber",
        "descripcion": "Empresa nueva e innovadora en el sector tecnológico",
        "fundador": "Kristof Henningsen",
        "estado": "Recientemente creada",
        "enfoque": "Soluciones tecnológicas innovadoras",
        "industria": "Tecnología",
    }


@tool
def obtener_info_kristof() -> dict:
    """
    Obtiene información detallada sobre Kristof Henningsen, fundador de Rekaliber.

    Usa esta herramienta cuando el usuario pregunte sobre:
    - Kristof o Kristoff
    - El fundador de Rekaliber
    - Biografía de Kristof
    - De dónde es Kristof
    - Dónde vive Kristof
    - Origen o nacionalidad de Kristof

    Returns:
        dict: Información personal y profesional de Kristof
    """
    return {
        "nombre_completo": "Kristof Henningsen",
        "rol": "Fundador y CEO de Rekaliber",
        "nacionalidad": "Boliviano",
        "lugar_nacimiento": "Oruro, Bolivia",
        "residencia_actual": "Suecia",
        "perfil": "Empresario boliviano con visión internacional",
        "descripcion": "Emprendedor tecnológico que conecta Bolivia con Suecia",
        "logros": [
            "Fundador de Rekaliber",
            "Empresario establecido en Suecia",
            "Promotor de innovación tecnológica",
            "Puente entre el ecosistema boliviano y europeo",
        ],
    }
