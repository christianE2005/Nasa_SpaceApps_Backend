from pydantic import BaseModel
from typing import Dict, Any, Optional

class SessionCreate(BaseModel):
    parametros: Dict[str, Any]
    user_id: int

class SessionResponse(BaseModel):
    id: int
    parametros: Dict[str, Any]
    csv_s3_key: Optional[str] = None
    csv_url: Optional[str] = None
    user_id: int
    
    class Config:
        from_attributes = True
