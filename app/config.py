from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos
MONGO_URI = os.getenv("CONNECTION_STRING")
