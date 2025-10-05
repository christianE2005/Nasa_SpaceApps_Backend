# tests/test_s3.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.domain.tools.s3_tools import S3Tools
from src.schemas.s3_schemas import S3UploadRequest, S3DownloadRequest, S3DeleteRequest

def test_upload_csv():
    # Prueba subir un CSV a S3
    
    # Crear contenido CSV de prueba
    csv_content = """nombre,edad,ciudad
Juan,25,Monterrey
Maria,30,CDMX
Pedro,28,Guadalajara"""
    
    # Convertir a bytes
    csv_bytes = csv_content.encode('utf-8')
    
    # Crear request
    upload_request = S3UploadRequest(
        user_id=1,
        session_id=123,
        file_content=csv_bytes,
        filename="test_data.csv"
    )
    
    # Subir a S3
    print("Subiendo CSV a S3...")
    response = S3Tools.upload_object(upload_request)
    
    if response.success:
        print("Archivo subido exitosamente!")
        print(f"Bucket: {response.bucket}")
        print(f"Key: {response.object_key}")
        print(f"URL: {response.url}")
    else:
        print("Error al subir archivo")
    
    return response


def test_download_csv(s3_key: str):
    # Prueba descargar un CSV de S3
    
    download_request = S3DownloadRequest(s3_key=s3_key)
    
    print(f"\nDescargando CSV desde S3...")
    print(f"Key: {s3_key}")
    
    try:
        content = S3Tools.download_object(download_request)
        print("Archivo descargado exitosamente!")
        print("\nContenido:")
        print(content)
        return content
    except Exception as e:
        print(f"Error al descargar: {str(e)}")
        return None


def test_delete_csv(s3_key: str):
    # Prueba eliminar un CSV de S3
    
    delete_request = S3DeleteRequest(s3_key=s3_key)
    
    print(f"\nEliminando archivo de S3...")
    print(f"Key: {s3_key}")
    
    response = S3Tools.delete_object(delete_request)
    
    if response.success:
        print("Archivo eliminado exitosamente!")
    else:
        print("Error al eliminar archivo")
    
    return response


if __name__ == "__main__":
    print("Iniciando pruebas de S3...\n")
    
    # 1. Subir archivo
    upload_response = test_upload_csv()
    
    if upload_response.success:
        # 2. Descargar el archivo que acabamos de subir
        test_download_csv(upload_response.object_key)
        # 3. Eliminar el archivo
        test_delete_csv(upload_response.object_key)