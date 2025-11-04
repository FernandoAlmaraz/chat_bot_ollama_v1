import sqlite3
import os

DB_PATH = "../data/propiedades.db"


def inicializar_db():
    """Crea la base de datos y tabla de propiedades con datos de ejemplo"""

    # Crear carpeta data si no existe
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla de propiedades
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS propiedades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            ciudad TEXT NOT NULL,
            zona TEXT,
            precio REAL NOT NULL,
            dormitorios INTEGER,
            banos INTEGER,
            area_m2 REAL,
            descripcion TEXT,
            disponible INTEGER DEFAULT 1
        )
    """
    )

    # Crear tabla de usuarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            email TEXT UNIQUE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Crear tabla de conversaciones
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            titulo TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """
    )

    # Crear tabla de mensajes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversacion_id INTEGER NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('usuario', 'asistente', 'sistema')),
            contenido TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversacion_id) REFERENCES conversaciones(id) ON DELETE CASCADE
        )
    """
    )

    # Crear índices para mejorar el rendimiento
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_conversaciones_usuario ON conversaciones(usuario_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_mensajes_conversacion ON mensajes(conversacion_id)"
    )

    # Verificar si ya hay datos
    cursor.execute("SELECT COUNT(*) FROM propiedades")
    if cursor.fetchone()[0] == 0:
        # Insertar datos de ejemplo
        propiedades_ejemplo = [
            (
                "Casa",
                "La Paz",
                "Calacoto",
                250000,
                4,
                3,
                180,
                "Casa moderna con jardín",
                1,
            ),
            (
                "Departamento",
                "La Paz",
                "Sopocachi",
                120000,
                2,
                2,
                85,
                "Departamento céntrico",
                1,
            ),
            (
                "Casa",
                "La Paz",
                "Achumani",
                350000,
                5,
                4,
                250,
                "Casa con vista panorámica",
                1,
            ),
            (
                "Departamento",
                "Santa Cruz",
                "Equipetrol",
                180000,
                3,
                2,
                110,
                "Depa amoblado",
                1,
            ),
            (
                "Casa",
                "Cochabamba",
                "Cala Cala",
                200000,
                3,
                2,
                150,
                "Casa con piscina",
                1,
            ),
            (
                "Terreno",
                "La Paz",
                "Mallasa",
                80000,
                0,
                0,
                500,
                "Terreno para construir",
                1,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO propiedades 
            (tipo, ciudad, zona, precio, dormitorios, banos, area_m2, descripcion, disponible)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            propiedades_ejemplo,
        )

        print(
            f"✅ Base de datos creada con {len(propiedades_ejemplo)} propiedades de ejemplo"
        )
    else:
        print("✅ Tabla de propiedades ya contiene datos")

    # Verificar y crear usuario por defecto si no existe
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO usuarios (nombre, email) VALUES (?, ?)",
            ("Usuario Demo", "demo@example.com"),
        )
        print("✅ Usuario demo creado")

    print("✅ Base de datos inicializada correctamente")
    print("   - Tabla: propiedades")
    print("   - Tabla: usuarios")
    print("   - Tabla: conversaciones")
    print("   - Tabla: mensajes")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    inicializar_db()
