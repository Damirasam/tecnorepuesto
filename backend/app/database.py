# Configuración de la base de datos
import os

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Conectando a la base de datos en: {DATABASE_URL}")