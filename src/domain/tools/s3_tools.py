from typing import List
from src.schemas.s3_schemas import (
    S3ListRequest, S3ListResponse, S3Object, S3UploadRequest, S3OperationResponse,
    S3DownloadRequest, S3DeleteRequest, S3ShareRequest, ShareS3Response,
)
from src.services.s3_service import S3Service


class S3Tools:
    @staticmethod
    def upload_object(request: S3UploadRequest) -> S3OperationResponse:
        # Sube un archivo CSV a S3
        s3_service = S3Service()
        
        try:
            # Subir archivo a S3
            s3_key = s3_service.upload_csv(
                file_content=request.file_content,
                user_id=request.user_id,
                session_id=request.session_id,
                filename=request.filename
            )
            
            # Obtener URL pública
            url = s3_service.get_file_url(s3_key)
            
            return S3OperationResponse(
                success=True,
                bucket=s3_service.bucket_name,
                object_key=s3_key,
                url=url
            )
        except Exception as e:
            print(f"Error en upload_object: {str(e)}")
            import traceback
            traceback.print_exc()
            return S3OperationResponse(
                success=False,
                bucket=s3_service.bucket_name if hasattr(s3_service, 'bucket_name') else "",
                object_key="",
                url=None
            )
    
    @staticmethod
    def download_object(request: S3DownloadRequest) -> str:
        # Descarga un archivo CSV de S3
        

        s3_service = S3Service()
        return s3_service.download_csv(request.s3_key)
    
    @staticmethod
    def delete_object(request: S3DeleteRequest) -> S3OperationResponse:
       # Elimina un archivo de S3

        s3_service = S3Service()
        
        try:
            success = s3_service.delete_csv(request.s3_key)
            
            return S3OperationResponse(
                success=success,
                bucket=s3_service.bucket_name,
                object_key=request.s3_key,
                url=None
            )
        except Exception as e:
            return S3OperationResponse(
                success=False,
                bucket=s3_service.bucket_name,
                object_key=request.s3_key,
                url=None
            )
