import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any


DB_PATH = "data/propiedades.db"


def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
    return conn


# ===== FUNCIONES DE USUARIOS =====


def obtener_o_crear_usuario(nombre: str = "Usuario Demo", email: str = "demo@example.com") -> int:
    """
    Obtiene el ID de un usuario existente o crea uno nuevo.

    Args:
        nombre: Nombre del usuario
        email: Email del usuario (debe ser único)

    Returns:
        ID del usuario
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Intentar obtener usuario existente
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    result = cursor.fetchone()

    if result:
        usuario_id = result[0]
    else:
        # Crear nuevo usuario
        cursor.execute(
            "INSERT INTO usuarios (nombre, email) VALUES (?, ?)",
            (nombre, email)
        )
        usuario_id = cursor.lastrowid
        conn.commit()

    conn.close()
    return usuario_id


def obtener_usuario(usuario_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene información de un usuario por ID"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return dict(result)
    return None


# ===== FUNCIONES DE CONVERSACIONES =====


def crear_conversacion(usuario_id: int, titulo: Optional[str] = None) -> int:
    """
    Crea una nueva conversación para un usuario.

    Args:
        usuario_id: ID del usuario
        titulo: Título opcional para la conversación

    Returns:
        ID de la conversación creada
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO conversaciones (usuario_id, titulo) VALUES (?, ?)",
        (usuario_id, titulo or "Nueva conversación")
    )
    conversacion_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return conversacion_id


def obtener_conversacion(conversacion_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene información de una conversación por ID"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM conversaciones WHERE id = ?", (conversacion_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return dict(result)
    return None


def listar_conversaciones_usuario(usuario_id: int, limite: int = 50) -> List[Dict[str, Any]]:
    """
    Lista las conversaciones de un usuario ordenadas por fecha de actualización.

    Args:
        usuario_id: ID del usuario
        limite: Número máximo de conversaciones a devolver

    Returns:
        Lista de conversaciones
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM conversaciones
        WHERE usuario_id = ?
        ORDER BY fecha_actualizacion DESC
        LIMIT ?
        """,
        (usuario_id, limite)
    )
    results = cursor.fetchall()
    conn.close()

    return [dict(row) for row in results]


def actualizar_fecha_conversacion(conversacion_id: int):
    """Actualiza la fecha de última modificación de una conversación"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE conversaciones SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?",
        (conversacion_id,)
    )

    conn.commit()
    conn.close()


def actualizar_titulo_conversacion(conversacion_id: int, titulo: str):
    """Actualiza el título de una conversación"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE conversaciones SET titulo = ?, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?",
        (titulo, conversacion_id)
    )

    conn.commit()
    conn.close()


# ===== FUNCIONES DE MENSAJES =====


def guardar_mensaje(
    conversacion_id: int,
    rol: str,
    contenido: str,
    actualizar_conversacion: bool = True
) -> int:
    """
    Guarda un mensaje en la base de datos.

    Args:
        conversacion_id: ID de la conversación
        rol: Rol del mensaje ('usuario', 'asistente', 'sistema')
        contenido: Contenido del mensaje
        actualizar_conversacion: Si True, actualiza la fecha de la conversación

    Returns:
        ID del mensaje creado
    """
    if rol not in ['usuario', 'asistente', 'sistema']:
        raise ValueError(f"Rol inválido: {rol}. Debe ser 'usuario', 'asistente' o 'sistema'")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO mensajes (conversacion_id, rol, contenido) VALUES (?, ?, ?)",
        (conversacion_id, rol, contenido)
    )
    mensaje_id = cursor.lastrowid

    if actualizar_conversacion:
        cursor.execute(
            "UPDATE conversaciones SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?",
            (conversacion_id,)
        )

    conn.commit()
    conn.close()

    return mensaje_id


def obtener_mensajes_conversacion(
    conversacion_id: int,
    limite: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Obtiene todos los mensajes de una conversación ordenados por fecha.

    Args:
        conversacion_id: ID de la conversación
        limite: Límite opcional de mensajes a devolver (los más recientes)

    Returns:
        Lista de mensajes
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if limite:
        cursor.execute(
            """
            SELECT * FROM mensajes
            WHERE conversacion_id = ?
            ORDER BY fecha_creacion DESC
            LIMIT ?
            """,
            (conversacion_id, limite)
        )
        # Invertir para tener orden cronológico
        results = cursor.fetchall()[::-1]
    else:
        cursor.execute(
            """
            SELECT * FROM mensajes
            WHERE conversacion_id = ?
            ORDER BY fecha_creacion ASC
            """,
            (conversacion_id,)
        )
        results = cursor.fetchall()

    conn.close()

    return [dict(row) for row in results]


def contar_mensajes_conversacion(conversacion_id: int) -> int:
    """Cuenta el número de mensajes en una conversación"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM mensajes WHERE conversacion_id = ?",
        (conversacion_id,)
    )
    count = cursor.fetchone()[0]
    conn.close()

    return count


def eliminar_conversacion(conversacion_id: int):
    """
    Elimina una conversación y todos sus mensajes (CASCADE).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM conversaciones WHERE id = ?", (conversacion_id,))

    conn.commit()
    conn.close()
