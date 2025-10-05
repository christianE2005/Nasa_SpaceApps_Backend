from __future__ import annotations

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class UnequalityIndicatorsBase(BaseModel):
    cve_ent: int
    cve_mun: int
    cve_sun: str
    cvegeo: str
    sun: str
    gmu: Optional[str] = None
    iisu_sun: Optional[str] = None
    iisu_cd: Optional[str] = None

    POBTOT: int

    Empleo: Optional[int] = None
    E_basica: Optional[int] = None
    E_media: Optional[int] = None
    E_superior: Optional[int] = None
    Salud_cama: Optional[int] = None
    Salud_cons: Optional[int] = None
    Abasto: Optional[int] = None
    Espacio_ab: Optional[int] = None
    Cultura: Optional[int] = None
    Est_Tpte: Optional[int] = None

    geometry_wkt: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class UnequalityIndicatorsCreate(UnequalityIndicatorsBase):
    pass


class UnequalityIndicatorsUpdate(BaseModel):
    cve_ent: Optional[int] = None
    cve_mun: Optional[int] = None
    cve_sun: Optional[str] = None
    cvegeo: Optional[str] = None
    sun: Optional[str] = None
    gmu: Optional[str] = None
    iisu_sun: Optional[str] = None
    iisu_cd: Optional[str] = None

    POBTOT: Optional[int] = None

    Empleo: Optional[int] = None
    E_basica: Optional[int] = None
    E_media: Optional[int] = None
    E_superior: Optional[int] = None
    Salud_cama: Optional[int] = None
    Salud_cons: Optional[int] = None
    Abasto: Optional[int] = None
    Espacio_ab: Optional[int] = None
    Cultura: Optional[int] = None
    Est_Tpte: Optional[int] = None

    geometry_wkt: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class UnequalityIndicatorsOut(UnequalityIndicatorsBase):
    id: UUID = Field(..., description="Resource UUID")
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
