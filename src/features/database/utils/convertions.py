import re
import unicodedata

def create_slug(input_string:str):
    # Convertir a minúsculas
    input_string = input_string.lower()
    
    # Normalizar la cadena para eliminar acentos y otros caracteres diacríticos
    input_string = unicodedata.normalize('NFKD', input_string)
    input_string = input_string.encode('ascii', 'ignore').decode('ascii')
    
    # Reemplazar espacios y otros caracteres por guiones
    input_string = re.sub(r'\s+', '-', input_string)
    
    # Eliminar cualquier carácter que no sea alfanumérico, guiones o espacios
    input_string = re.sub(r'[^a-z0-9\-]', '', input_string)
    
    # Eliminar guiones consecutivos
    input_string = re.sub(r'-+', '-', input_string)
    
    # Eliminar guiones al principio y al final de la cadena
    input_string = input_string.strip('-')
    
    return input_string


def list_to_pagination_list(list:list, per_page:int = 10):
    totals =  len(list)
    sublistas = [list[i:i+per_page] for i in range(0, totals, per_page)]

    return {
        'total':totals,
        'data': sublistas,
        'per_page':  per_page,
        'last_page': len(sublistas) - 1
    }

