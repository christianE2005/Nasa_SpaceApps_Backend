from __future__ import annotations

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UrbanQualityBase(BaseModel):
    lat: float
    lon: float
    POBTOT: int

    GRAPROES: Optional[float] = None
    GRAPROES_F: Optional[float] = None
    GRAPROES_M: Optional[float] = None

    RECUCALL_C: Optional[int] = None
    RAMPAS_C: Optional[int] = None
    PASOPEAT_C: Optional[int] = None
    BANQUETA_C: Optional[int] = None
    GUARNICI_C: Optional[int] = None
    CICLOVIA_C: Optional[int] = None
    CICLOCAR_C: Optional[int] = None
    ALUMPUB_C: Optional[int] = None
    LETRERO_C: Optional[int] = None
    TELPUB_C: Optional[int] = None
    ARBOLES_C: Optional[int] = None
    DRENAJEP_C: Optional[int] = None
    TRANSCOL_C: Optional[int] = None
    ACESOPER_C: Optional[int] = None
    ACESOAUT_C: Optional[int] = None

class UrbanQualityCreate(UrbanQualityBase):
    pass

class UrbanQualityUpdate(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None
    POBTOT: Optional[int] = None

    GRAPROES: Optional[float] = None
    GRAPROES_F: Optional[float] = None
    GRAPROES_M: Optional[float] = None

    RECUCALL_C: Optional[int] = None
    RAMPAS_C: Optional[int] = None
    PASOPEAT_C: Optional[int] = None
    BANQUETA_C: Optional[int] = None
    GUARNICI_C: Optional[int] = None
    CICLOVIA_C: Optional[int] = None
    CICLOCAR_C: Optional[int] = None
    ALUMPUB_C: Optional[int] = None
    LETRERO_C: Optional[int] = None
    TELPUB_C: Optional[int] = None
    ARBOLES_C: Optional[int] = None
    DRENAJEP_C: Optional[int] = None
    TRANSCOL_C: Optional[int] = None
    ACESOPER_C: Optional[int] = None
    ACESOAUT_C: Optional[int] = None

class UrbanQualityOut(UrbanQualityBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
