from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, String, Text
from src.core.models import UUIDPrimaryKey, Timestamp
from src.core.database import Base


class UnequalityIndicators(Base, UUIDPrimaryKey, Timestamp):
    __tablename__ = "unequality_indicators"

    # --- Identificadores / claves ---
    cve_ent: Mapped[int] = mapped_column(Integer, nullable=False)         
    cve_mun: Mapped[int] = mapped_column(Integer, nullable=False)         
    cve_sun: Mapped[str] = mapped_column(String(12), nullable=False)       
    cvegeo: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)  
    sun: Mapped[str] = mapped_column(String(128), nullable=False)          
    gmu: Mapped[str] = mapped_column(String(32), nullable=True)            
    iisu_sun: Mapped[str] = mapped_column(String(32), nullable=True)
    iisu_cd: Mapped[str] = mapped_column(String(32), nullable=True)

    # --- Población (map a nombre de columna real del CSV) ---
    POBTOT: Mapped[int] = mapped_column("Pob_2010", Integer, nullable=False)

    # --- Indicadores (según CSV: int-like) ---
    Empleo: Mapped[int] = mapped_column(Integer, nullable=True)
    E_basica: Mapped[int] = mapped_column(Integer, nullable=True)
    E_media: Mapped[int] = mapped_column(Integer, nullable=True)
    E_superior: Mapped[int] = mapped_column(Integer, nullable=True)
    Salud_cama: Mapped[int] = mapped_column(Integer, nullable=True)
    Salud_cons: Mapped[int] = mapped_column(Integer, nullable=True)
    Abasto: Mapped[int] = mapped_column(Integer, nullable=True)
    Espacio_ab: Mapped[int] = mapped_column(Integer, nullable=True)
    Cultura: Mapped[int] = mapped_column(Integer, nullable=True)
    Est_Tpte: Mapped[int] = mapped_column(Integer, nullable=True)

    # --- Geometría (WKT del CSV) + centroid opcional ---
    geometry_wkt: Mapped[str] = mapped_column("geometry", Text, nullable=True)
    lat: Mapped[float] = mapped_column(Float, nullable=True)  
    lon: Mapped[float] = mapped_column(Float, nullable=True)