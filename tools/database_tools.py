from langchain_core.tools import tool
import sqlite3
from typing import Optional, List, Dict, Any

# Ruta a la base de datos
DB_PATH = "data/propiedades.db"


@tool
def buscar_propiedades(
    tipo: Optional[str] = None,
    ciudad: Optional[str] = None,
    precio_max: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """
    Busca propiedades en la base de datos según criterios.

    Usa esta herramienta cuando el usuario pregunte sobre:
    - Propiedades disponibles
    - Casas, departamentos o terrenos
    - Propiedades en una ciudad específica
    - Propiedades dentro de un presupuesto

    Args:
        tipo: Tipo de propiedad (Casa, Departamento, Terreno)
        ciudad: Ciudad (La Paz, Santa Cruz, Cochabamba)
        precio_max: Precio máximo en dólares

    Returns:
        Lista de propiedades que cumplen los criterios
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT * FROM propiedades WHERE disponible = 1"
        params = []

        if tipo:
            query += " AND tipo LIKE ?"
            params.append(f"%{tipo}%")

        if ciudad:
            query += " AND ciudad LIKE ?"
            params.append(f"%{ciudad}%")

        if precio_max:
            query += " AND precio <= ?"
            params.append(precio_max)

        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()

        propiedades = []
        for row in resultados:
            propiedades.append(
                {
                    "id": row["id"],
                    "tipo": row["tipo"],
                    "ciudad": row["ciudad"],
                    "zona": row["zona"],
                    "precio": row["precio"],
                    "dormitorios": row["dormitorios"],
                    "descripcion": row["descripcion"],
                }
            )

        return propiedades if propiedades else []

    except Exception as e:
        return [{"error": str(e)}]


@tool
def contar_propiedades(ciudad: Optional[str] = None) -> Dict[str, Any]:
    """
    Cuenta cuántas propiedades hay disponibles.

    Usa cuando pregunten:
    - Cuántas propiedades hay
    - Cantidad de propiedades disponibles
    - Estadísticas de propiedades

    Args:
        ciudad: Filtrar por ciudad (opcional)

    Returns:
        Diccionario con el conteo total y por tipo
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if ciudad:
            cursor.execute(
                """
                SELECT tipo, COUNT(*) as cantidad 
                FROM propiedades 
                WHERE disponible = 1 AND ciudad LIKE ?
                GROUP BY tipo
            """,
                (f"%{ciudad}%",),
            )
        else:
            cursor.execute(
                """
                SELECT tipo, COUNT(*) as cantidad 
                FROM propiedades 
                WHERE disponible = 1
                GROUP BY tipo
            """
            )

        resultados = cursor.fetchall()
        conn.close()

        conteo = {"total": 0, "por_tipo": {}}
        for tipo, cantidad in resultados:
            conteo["por_tipo"][tipo] = cantidad
            conteo["total"] += cantidad

        if ciudad:
            conteo["ciudad"] = ciudad

        return conteo

    except Exception as e:
        return {"error": str(e)}
