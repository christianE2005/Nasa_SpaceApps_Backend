from typing import Dict, Any, Tuple, Optional
import asyncpg
from shapely.geometry import shape, mapping
from shapely.ops import transform as shp_transform
from shapely import wkt as shp_wkt
import json

# Conversión simple grados↔metros (aprox) si necesitas buffers rápidos
def meters_to_deg(lat: float, meters: float) -> Tuple[float, float]:
    deg_lat = meters / 111_320.0
    deg_lon = meters / (111_320.0 * max(0.1, abs(__import__("math").cos(__import__("math").radians(lat)))))
    return deg_lat, deg_lon

class ContextBuilder:
    """
    Arma los payloads para:
      - PopulationRequest (tool City Infrastructure Model)
      - UnequalityIndicatorsRequest (tool Population Inequality Model)
    a partir de una geometry (GeoJSON) o lat/lon.
    Hace el query inicial a tu base (ej. Postgres con PostGIS).
    """

    def __init__(self, dsn: str):
        self.dsn = dsn

    async def _conn(self):
        return await asyncpg.connect(self.dsn)

    async def build_population_payload(
        self, geometry: Dict[str, Any], lat: float, lon: float
    ) -> Dict[str, Any]:
        """
        Devuelve dict con TODOS los campos exigidos por PopulationRequest.
        Aquí se muestran consultas ejemplo; ajusta nombres de tablas/campos.
        """
        # Ejemplo: usa centroid para asociar zona censal
        g = shape(geometry)
        c = g.centroid
        lat_c, lon_c = c.y, c.x

        sql = """
        WITH target AS (
          SELECT geom
          FROM census_blocks
          WHERE ST_Contains(geom, ST_SetSRID(ST_Point($1, $2), 4326))
          LIMIT 1
        )
        SELECT
          pobtot, pobmas, pobfem,
          pob0_14, pob15_29, pob30_59, p_60,
          p_cd_t, graproes, graproes_f, graproes_m,
          vivtot, vivpar, tvipahab, vivnohab,
          prom_ocup, pro_ocup_c, v3masocu, v3masocu_p,
          vph_pidt, vph_pidt_p, vph_c_el, vph_c_el_p, vph_exsa, vph_exsa_p,
          vph_dren, vph_dren_p,
          recucall_c, rampas_c, pasopeat_c, banqueta_c, guarnici_c,
          ciclovia_c, ciclocar_c, alumpub_c, letrero_c, telpub_c,
          arboles_c, drenajep_c, transcol_c, acesoper_c, acesoaut_c,
          puessemi_c, puesambu_c
        FROM urban_features
        WHERE ST_Intersects(geom, (SELECT geom FROM target))
        LIMIT 1;
        """

        async with await self._conn() as con:
            row = await con.fetchrow(sql, lon_c, lat_c)

        # Fallbacks sencillos si faltan datos
        def d(name, default):
            return row[name] if row and row[name] is not None else default

        payload = {
            "pobtot": d("pobtot", 0),
            "pobmas": d("pobmas", 0),
            "pobfem": d("pobfem", 0),
            "pob0_14": d("pob0_14", 0),
            "pob15_29": d("pob15_29", 0),
            "pob30_59": d("pob30_59", 0),
            "p_60": d("p_60", 0),
            "p_cd_t": d("p_cd_t", 0),
            "graproes": d("graproes", 0.0),
            "graproes_f": d("graproes_f", 0.0),
            "graproes_m": d("graproes_m", 0.0),

            "vivtot": d("vivtot", 0),
            "vivpar": d("vivpar", 0),
            "tvipahab": d("tvipahab", 0),
            "vivnohab": d("vivnohab", 0),
            "prom_ocup": d("prom_ocup", 0.0),
            "pro_ocup_c": d("pro_ocup_c", 0.0),
            "v3masocu": d("v3masocu", 0),
            "v3masocu_p": d("v3masocu_p", 0.0),

            "vph_pidt": d("vph_pidt", 0),
            "vph_pidt_p": d("vph_pidt_p", 0.0),
            "vph_c_el": d("vph_c_el", 0),
            "vph_c_el_p": d("vph_c_el_p", 0.0),
            "vph_exsa": d("vph_exsa", 0),
            "vph_exsa_p": d("vph_exsa_p", 0.0),
            "vph_dren": d("vph_dren", 0),
            "vph_dren_p": d("vph_dren_p", 0.0),

            "recucall_c": d("recucall_c", "paved"),
            "rampas_c": d("rampas_c", False),
            "pasopeat_c": d("pasopeat_c", False),
            "banqueta_c": d("banqueta_c", False),
            "guarnici_c": d("guarnici_c", False),
            "ciclovia_c": d("ciclovia_c", False),
            "ciclocar_c": d("ciclocar_c", False),
            "alumpub_c": d("alumpub_c", False),
            "letrero_c": d("letrero_c", False),
            "telpub_c": d("telpub_c", False),
            "arboles_c": d("arboles_c", False),
            "drenajep_c": d("drenajep_c", False),
            "transcol_c": d("transcol_c", False),
            "acesoper_c": d("acesoper_c", False),
            "acesoaut_c": d("acesoaut_c", False),
            "puessemi_c": d("puessemi_c", False),
            "puesambu_c": d("puesambu_c", False),

            "lat": float(lat),
            "lon": float(lon),
        }
        return payload

    async def build_inequality_payload(
        self, geometry: Dict[str, Any], lat: float, lon: float
    ) -> Dict[str, Any]:
        """
        Devuelve dict con TODOS los campos exigidos por UnequalityIndicatorsRequest.
        Incluye wkt y códigos de entidad/municipio consultados por punto.
        """
        g = shape(geometry)
        c = g.centroid
        lat_c, lon_c = c.y, c.x
        wkt_str = g.wkt  # geometry_wkt

        sql = """
        SELECT
          cve_ent, cve_mun, cve_sun, cvegeo, sun, gmu, iisu_sun, iisu_cd,
          pobtot as "POBTOT",
          empleo as "Empleo",
          e_basica as "E_basica",
          e_media as "E_media",
          e_superior as "E_superior",
          salud_cama as "Salud_cama",
          salud_cons as "Salud_cons",
          abasto as "Abasto",
          espacio_ab as "Espacio_ab",
          cultura as "Cultura",
          est_tpte as "Est_Tpte"
        FROM inequality_indicators
        WHERE ST_Contains(geom, ST_SetSRID(ST_Point($1, $2), 4326))
        LIMIT 1;
        """

        async with await self._conn() as con:
            row = await con.fetchrow(sql, lon_c, lat_c)

        def d(name, default):
            return row[name] if row and row[name] is not None else default

        payload = {
            "cve_ent": d("cve_ent", 0),
            "cve_mun": d("cve_mun", 0),
            "cve_sun": d("cve_sun", ""),
            "cvegeo": d("cvegeo", ""),
            "sun": d("sun", ""),
            "gmu": d("gmu", ""),
            "iisu_sun": d("iisu_sun", ""),
            "iisu_cd": d("iisu_cd", ""),

            "POBTOT": d("POBTOT", 0),
            "Empleo": d("Empleo", 0),
            "E_basica": d("E_basica", 0),
            "E_media": d("E_media", 0),
            "E_superior": d("E_superior", 0),
            "Salud_cama": d("Salud_cama", 0),
            "Salud_cons": d("Salud_cons", 0),
            "Abasto": d("Abasto", 0),
            "Espacio_ab": d("Espacio_ab", 0),
            "Cultura": d("Cultura", 0),
            "Est_Tpte": d("Est_Tpte", 0),

            "geometry_wkt": wkt_str,
            "lat": float(lat),
            "lon": float(lon),
        }
        return payload
