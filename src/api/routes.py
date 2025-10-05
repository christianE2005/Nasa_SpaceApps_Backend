"""
Endpoints de la API para consultas de datos de calidad urbana.
Los endpoints reciben coordenadas lat/lon min/max desde el frontend y devuelven
datos filtrados por área geográfica.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.services import service
from src.schemas.urban_quality import PopulationData, EducationData, TreesData

# Router con prefijo para todos los endpoints
router = APIRouter(prefix="/api/v1", tags=["Urban Quality Data"])


@router.get("/population", response_model=List[PopulationData])
def get_population_data(
    lat_min: float = Query(..., description="Latitud mínima del área", example=19.4),
    lat_max: float = Query(..., description="Latitud máxima del área", example=19.5),
    lon_min: float = Query(..., description="Longitud mínima del área", example=-99.2),
    lon_max: float = Query(..., description="Longitud máxima del área", example=-99.1),
    db: Session = Depends(get_db)
):
    """
    **Endpoint 1: Datos de Población Total**
    
    Retorna todos los puntos geográficos dentro del área especificada con:
    - `lat`: Latitud del punto
    - `lon`: Longitud del punto
    - `POBTOT`: Población total
    
    **Parámetros:**
    - **lat_min**: Latitud mínima del rectángulo a consultar
    - **lat_max**: Latitud máxima del rectángulo a consultar
    - **lon_min**: Longitud mínima del rectángulo a consultar
    - **lon_max**: Longitud máxima del rectángulo a consultar
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/population?lat_min=19.4&lat_max=19.5&lon_min=-99.2&lon_max=-99.1
    ```
    """
    try:
        results = service.get_population_by_area(db, lat_min, lat_max, lon_min, lon_max)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar datos: {str(e)}")


@router.get("/education", response_model=List[EducationData])
def get_education_data(
    lat_min: float = Query(..., description="Latitud mínima del área", example=19.4),
    lat_max: float = Query(..., description="Latitud máxima del área", example=19.5),
    lon_min: float = Query(..., description="Longitud mínima del área", example=-99.2),
    lon_max: float = Query(..., description="Longitud máxima del área", example=-99.1),
    db: Session = Depends(get_db)
):
    """
    **Endpoint 2: Datos de Grado Promedio de Escolaridad**
    
    Retorna todos los puntos geográficos dentro del área especificada con:
    - `lat`: Latitud del punto
    - `lon`: Longitud del punto
    - `GRAPROES`: Grado promedio de escolaridad (general)
    - `GRAPROES_F`: Grado promedio de escolaridad (femenino)
    - `GRAPROES_M`: Grado promedio de escolaridad (masculino)
    
    **Parámetros:**
    - **lat_min**: Latitud mínima del rectángulo a consultar
    - **lat_max**: Latitud máxima del rectángulo a consultar
    - **lon_min**: Longitud mínima del rectángulo a consultar
    - **lon_max**: Longitud máxima del rectángulo a consultar
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/education?lat_min=19.4&lat_max=19.5&lon_min=-99.2&lon_max=-99.1
    ```
    """
    try:
        results = service.get_education_by_area(db, lat_min, lat_max, lon_min, lon_max)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar datos: {str(e)}")


@router.get("/trees", response_model=List[TreesData])
def get_trees_data(
    lat_min: float = Query(..., description="Latitud mínima del área", example=19.4),
    lat_max: float = Query(..., description="Latitud máxima del área", example=19.5),
    lon_min: float = Query(..., description="Longitud mínima del área", example=-99.2),
    lon_max: float = Query(..., description="Longitud máxima del área", example=-99.1),
    db: Session = Depends(get_db)
):
    """
    **Endpoint 3: Datos de Árboles en la Calle**
    
    Retorna todos los puntos geográficos dentro del área especificada con:
    - `lat`: Latitud del punto
    - `lon`: Longitud del punto
    - `ARBOLES_C`: Cantidad de árboles en la calle
    
    **Parámetros:**
    - **lat_min**: Latitud mínima del rectángulo a consultar
    - **lat_max**: Latitud máxima del rectángulo a consultar
    - **lon_min**: Longitud mínima del rectángulo a consultar
    - **lon_max**: Longitud máxima del rectángulo a consultar
    
    **Ejemplo de uso:**
    ```
    GET /api/v1/trees?lat_min=19.4&lat_max=19.5&lon_min=-99.2&lon_max=-99.1
    ```
    """
    try:
        results = service.get_trees_by_area(db, lat_min, lat_max, lon_min, lon_max)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar datos: {str(e)}")
