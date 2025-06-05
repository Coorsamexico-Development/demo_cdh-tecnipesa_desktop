import sys
import os

def resource_path(*relative_paths):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, *relative_paths)
    return os.path.join(os.getcwd(), *relative_paths)

# Ejemplo de uso
#ruta_logo = resource_path('assets/logo.png')