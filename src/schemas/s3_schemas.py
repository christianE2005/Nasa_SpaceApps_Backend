from pydantic import BaseModel
from typing import Optional, List


class S3UploadRequest(BaseModel):
    """Request para subir archivo a S3"""
    user_id: int
    session_id: int
    file_content: bytes
    filename: Optional[str] = "data.csv"
    
    class Config:
        arbitrary_types_allowed = True


class S3OperationResponse(BaseModel):
    """Response de operaciones en S3"""
    success: bool
    bucket: str
    object_key: str
    url: Optional[str] = None


class S3DownloadRequest(BaseModel):
    """Request para descargar archivo de S3"""
    s3_key: str


class S3DeleteRequest(BaseModel):
    """Request para eliminar archivo de S3"""
    s3_key: str


class S3ShareRequest(BaseModel):
    """Request para compartir/generar URL presignada"""
    s3_key: str
    expiration: Optional[int] = 3600  # segundos


class ShareS3Response(BaseModel):
    """Response con URL presignada"""
    success: bool
    presigned_url: Optional[str] = None
    expiration: int


class S3Object(BaseModel):
    """Representa un objeto en S3"""
    key: str
    size: int
    last_modified: str


class S3ListRequest(BaseModel):
    """Request para listar objetos en S3"""
    prefix: Optional[str] = None
    max_keys: Optional[int] = 1000


class S3ListResponse(BaseModel):
    """Response con lista de objetos"""
    success: bool
    objects: List[S3Object]
    count: int
