import sqlite3
import os

DB_PATH = "data/propiedades.db"


def inicializar_db():
    """Crea la base de datos y tabla de propiedades con datos de ejemplo"""

    # Crear carpeta data si no existe
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla
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
        print("✅ Base de datos ya existe")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    inicializar_db()
