from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, Integer
from src.core.models import UUIDPrimaryKey, Timestamp
from src.core.database import Base


class UrbanQuality(Base, UUIDPrimaryKey, Timestamp):
    __tablename__ = "urban_quality"

    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    POBTOT: Mapped[int] = mapped_column(Integer, nullable=False)

    GRAPROES: Mapped[float] = mapped_column(Float)
    GRAPROES_F: Mapped[float] = mapped_column(Float)
    GRAPROES_M: Mapped[float] = mapped_column(Float)

    RECUCALL_C: Mapped[int] = mapped_column(Integer)
    RAMPAS_C: Mapped[int] = mapped_column(Integer)
    PASOPEAT_C: Mapped[int] = mapped_column(Integer)
    BANQUETA_C: Mapped[int] = mapped_column(Integer)
    GUARNICI_C: Mapped[int] = mapped_column(Integer)
    CICLOVIA_C: Mapped[int] = mapped_column(Integer)
    CICLOCAR_C: Mapped[int] = mapped_column(Integer)
    ALUMPUB_C: Mapped[int] = mapped_column(Integer)
    LETRERO_C: Mapped[int] = mapped_column(Integer)
    TELPUB_C: Mapped[int] = mapped_column(Integer)
    ARBOLES_C: Mapped[int] = mapped_column(Integer)
    DRENAJEP_C: Mapped[int] = mapped_column(Integer)
    TRANSCOL_C: Mapped[int] = mapped_column(Integer)
    ACESOPER_C: Mapped[int] = mapped_column(Integer)
    ACESOAUT_C: Mapped[int] = mapped_column(Integer)
