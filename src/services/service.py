"""
Servicios para consultas a la base de datos de Urban Quality.
Contiene la lógica de negocio para filtrar datos por área geográfica.
"""

from sqlalchemy.orm import Session
from typing import List
from src.models.urban_quality import UrbanQuality


def get_population_by_area(
    db: Session,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float
) -> List[UrbanQuality]:
    """
    Obtiene datos de población total (POBTOT) filtrados por área geográfica.
    
    Args:
        db: Sesión de base de datos
        lat_min: Latitud mínima del área
        lat_max: Latitud máxima del área
        lon_min: Longitud mínima del área
        lon_max: Longitud máxima del área
    
    Returns:
        Lista de registros con lat, lon y POBTOT dentro del área especificada
    """
    return db.query(UrbanQuality)\
        .filter(
            UrbanQuality.lat.between(lat_min, lat_max),
            UrbanQuality.lon.between(lon_min, lon_max)
        )\
        .all()


def get_education_by_area(
    db: Session,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float
) -> List[UrbanQuality]:
    """
    Obtiene datos de grado promedio de escolaridad (GRAPROES, GRAPROES_F, GRAPROES_M)
    filtrados por área geográfica.
    
    Args:
        db: Sesión de base de datos
        lat_min: Latitud mínima del área
        lat_max: Latitud máxima del área
        lon_min: Longitud mínima del área
        lon_max: Longitud máxima del área
    
    Returns:
        Lista de registros con lat, lon y datos de escolaridad dentro del área especificada
    """
    return db.query(UrbanQuality)\
        .filter(
            UrbanQuality.lat.between(lat_min, lat_max),
            UrbanQuality.lon.between(lon_min, lon_max)
        )\
        .all()


def get_trees_by_area(
    db: Session,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float
) -> List[UrbanQuality]:
    """
    Obtiene datos de árboles en la calle (ARBOLES_C) filtrados por área geográfica.
    
    Args:
        db: Sesión de base de datos
        lat_min: Latitud mínima del área
        lat_max: Latitud máxima del área
        lon_min: Longitud mínima del área
        lon_max: Longitud máxima del área
    
    Returns:
        Lista de registros con lat, lon y ARBOLES_C dentro del área especificada
    """
    return db.query(UrbanQuality)\
        .filter(
            UrbanQuality.lat.between(lat_min, lat_max),
            UrbanQuality.lon.between(lon_min, lon_max)
        )\
        .all()
