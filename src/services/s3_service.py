import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from src.core.settings import Settings as settings

load_dotenv()

class S3Service:
    def __init__(self):
        self.bucket_name = os.getenv(settings.s3_bucket_name)
        self.region = os.getenv(settings.aws_region)

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv(settings.aws_access_key_id),
            aws_secret_access_key=os.getenv(settings.aws_secret_access_key),
            region_name=self.region
        )
    
    def upload_csv(self, file_content: bytes, user_id: int, session_id: int, filename: str) -> str:
        s3_key = f"usuarios/{user_id}/sesiones/{session_id}_{filename}"
        
        try: 
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType='text/csv'
            )
                
            return s3_key
        except ClientError as e:
            raise Exception(f"Error al subir archivo a S3: {str(e)}")
    
    def upload_csv_from_string(self, csv_string: str, user_id: int, session_id: int, filename: str) -> str:

        file_content = csv_string.encode('utf-8')
        return self.upload_csv(file_content, user_id, session_id, filename)
    
    def get_file_url(self, s3_key: str) -> str:
        return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
    
    def download_csv(self, s3_key: str) -> str:

        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            raise Exception(f"Error al descargar archivo de S3: {str(e)}")
    
    def delete_csv(self, s3_key: str) -> bool:
        # Elimina un archivo CSV de S3

        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError as e:
            raise Exception(f"Error al eliminar archivo de S3: {str(e)}")
    
    def file_exists(self, s3_key: str) -> bool:

        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError:
            return False
