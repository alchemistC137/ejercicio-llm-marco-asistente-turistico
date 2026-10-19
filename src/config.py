"""Módulo de configuración global."""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Validar que exista la API Key
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("Falta la variable GOOGLE_API_KEY en el archivo .env")

# Modelos de Google (basados en las últimas versiones estables)
GENERATION_MODEL = "gemini-flash-latest"
EMBEDDING_MODEL = "models/gemini-embedding-001"