from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal

class Geometry(BaseModel):
    """
    Representa una geometría GeoJSON (Point, Polygon o MultiPolygon).
    Ejemplo:
    {
      "type": "Polygon",
      "coordinates": [[[lon, lat], [lon, lat], ...]]
    }
    """
    type: Literal["Point", "Polygon", "MultiPolygon"]
    coordinates: Any

class ZoneIn(BaseModel):
    """
    Una zona individual a analizar.
    - id: identificador único
    - geometry: GeoJSON de la zona
    - data: atributos extra (opcional)
    """
    id: str = Field(..., description="Identificador único de la zona.")
    geometry: Geometry
    data: Dict[str, Any] = Field(default_factory=dict, description="Atributos adicionales opcionales")

class PlanRequest(BaseModel):
    """
    Request principal que recibe el endpoint /urban/run o /urban/stream.
    """
    zones: List[ZoneIn] = Field(..., description="Lista de zonas o polígonos a analizar.")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Filtros específicos para el análisis.")
    objectives: List[str] = Field(default_factory=list, description="Objetivos de planeación (ej. 'mejorar movilidad').")
