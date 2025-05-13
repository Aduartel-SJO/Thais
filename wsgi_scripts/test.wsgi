import sys
import os

# Añade el directorio de tu aplicación a sys.path
sys.path.insert(0, 'C:/xampp/htdocs/Antonio')

# Especifica el entorno de Python que Apache debe usar
sys.path.insert(0, 'C:/Python312/Lib/site-packages')

# Asegúrate de que Apache usa el Python correcto
os.environ['PYTHONHOME'] = 'C:/Python312'

# Importa la aplicación Flask
from run import app as application