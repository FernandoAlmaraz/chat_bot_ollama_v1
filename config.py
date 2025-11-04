import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración de la aplicación"""

    # Modelo
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:latest")
    MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.5"))

    # Flask
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # Base de datos
    DB_PATH = os.getenv("DB_PATH", "propiedades.db")
