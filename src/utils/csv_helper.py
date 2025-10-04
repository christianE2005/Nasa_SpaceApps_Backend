import csv
from io import StringIO
from typing import List, Dict

def csv_to_string(csv_file_path: str) -> str:

    # Lee un archivo CSV y lo convierte a string

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        return file.read()

def csv_to_bytes(csv_file_path: str) -> bytes:

    # Lee un archivo CSV y lo convierte a bytes

    with open(csv_file_path, 'rb') as file:
        return file.read()

def string_to_csv_list(csv_string: str) -> List[Dict]:

    # Convierte un string CSV a una lista de diccionarios
 
    csv_file = StringIO(csv_string)
    reader = csv.DictReader(csv_file)
    return list(reader)

def save_string_to_csv(csv_string: str, output_path: str):

    # Guarda un string CSV en un archivo

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(csv_string)

def dict_list_to_csv_string(data: List[Dict]) -> str:

    # Convierte una lista de diccionarios a string CSV

    if not data:
        return ""
    
    output = StringIO()
    fieldnames = data[0].keys()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    
    return output.getvalue()
