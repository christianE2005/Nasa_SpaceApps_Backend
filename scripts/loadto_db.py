"""Utility script for importing Excel datasets into the project's database."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Iterable, Optional, Tuple

import pandas as pd
from pandas import DataFrame
from sqlalchemy.orm import Session

# Add repository root to the module search path so that ``src`` imports work
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.core.database import SessionLocal  # noqa: E402
from src.models.urban_quality import UrbanQuality  # noqa: E402
from src.models.unequality_indicators import UnequalityIndicators  # noqa: E402


LOGGER = logging.getLogger("loadto_db")
DEFAULT_STATIC_DIR = ROOT_DIR / "Nasa_SpaceApps_Backend/static"
BATCH_SIZE = 500


def configure_logging(verbose: bool) -> None:
	"""Configure basic logging for the ETL run."""

	level = logging.DEBUG if verbose else logging.INFO
	logging.basicConfig(
		level=level,
		format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
		datefmt="%Y-%m-%d %H:%M:%S",
	)


def safe_int(value: object) -> Optional[int]:
	"""Convert *value* to :class:`int`, returning ``None`` when not possible."""

	if value is None:
		return None
	if isinstance(value, str) and not value.strip():
		return None
	try:
		if pd.isna(value):  # type: ignore[arg-type]
			return None
	except TypeError:
		# ``pd.isna`` raises TypeError for some objects; ignore and try casting.
		pass

	try:
		return int(float(value))
	except (TypeError, ValueError):
		return None


def safe_float(value: object) -> Optional[float]:
	"""Convert *value* to :class:`float`, returning ``None`` when not possible."""

	if value is None:
		return None
	if isinstance(value, str) and not value.strip():
		return None
	try:
		if pd.isna(value):  # type: ignore[arg-type]
			return None
	except TypeError:
		pass

	try:
		return float(value)
	except (TypeError, ValueError):
		return None


def safe_str(value: object) -> Optional[str]:
	"""Convert *value* to a UTF-8 safe :class:`str` (or ``None``)."""

	if value is None:
		return None
	if isinstance(value, str):
		text = value.strip()
		if not text:
			return None
		try:
			return text.encode("utf-8", errors="ignore").decode("utf-8")
		except Exception:  # pragma: no cover - defensive
			return text

	try:
		text = str(value).strip()
	except Exception:  # pragma: no cover - defensive
		return None

	return text or None


def read_excel(path: Path) -> DataFrame:
	"""Load an Excel file into a :class:`~pandas.DataFrame`."""

	LOGGER.info("Leyendo archivo: %s", path)
	df = pd.read_excel(path, engine="openpyxl")
	LOGGER.info("Archivo leído. Filas=%d, Columnas=%s", len(df), list(df.columns))
	return df


def log_error_summary(dataset: str, errors: Iterable[dict], destination: Path) -> None:
	"""Persist an error summary file for manual review."""

	if not errors:
		return


	destination.parent.mkdir(parents=True, exist_ok=True)
	with destination.open("w", encoding="utf-8") as file:
		file.write(f"ERRORES EN CARGA DE {dataset.upper()}\n")
		file.write("=" * 72 + "\n\n")
		for err in errors:
			file.write(f"Fila DataFrame: {err['row_index']}\n")
			file.write(f"Detalle: {err['error']}\n")
			extra = err.get("context")
			if extra:
				file.write(f"Contexto: {extra}\n")
			file.write("-" * 72 + "\n")

	LOGGER.warning("Detalles completos guardados en: %s", destination)


def commit_batch(
	db: Session,
	batch: list[Tuple[object, int, str]],
	errors: list[dict],
	label: str,
) -> int:
	"""Persist a batch of SQLAlchemy models with graceful degradation."""

	if not batch:
		return 0

	models = [item[0] for item in batch]
	try:
		db.add_all(models)
		db.commit()
		return len(models)
	except Exception as exc:  # pragma: no cover - depends on DB state
		LOGGER.error(
			"Error al insertar batch de %s (%d registros): %s",
			label,
			len(batch),
			exc,
		)
		db.rollback()

		inserted = 0
		for model, idx, context in batch:
			try:
				db.add(model)
				db.commit()
				inserted += 1
			except Exception as inner_exc:  # pragma: no cover - DB specific
				db.rollback()
				errors.append(
					{
						"row_index": idx,
						"error": str(inner_exc),
						"context": context,
					}
				)
		return inserted
	finally:
		db.expunge_all()


def load_urban_quality(df: DataFrame, db: Session, error_dir: Path) -> Tuple[int, int]:
	"""Persist Urban Quality rows into the database."""

	required_columns = {"lat", "lon", "POBTOT"}
	missing_cols = required_columns - set(df.columns)
	if missing_cols:
		raise ValueError(
			f"El archivo de Urban Quality no contiene las columnas obligatorias: {missing_cols}"
		)

	loaded, skipped = 0, 0
	errors = []

	batch: list[Tuple[UrbanQuality, int, str]] = []

	for idx, row in df.iterrows():
		lat = safe_float(row.get("lat"))
		lon = safe_float(row.get("lon"))
		pobtot = safe_int(row.get("POBTOT"))

		if lat is None or lon is None or pobtot is None:
			skipped += 1
			continue

		record = UrbanQuality(
			lat=lat,
			lon=lon,
			POBTOT=pobtot,
			GRAPROES=safe_float(row.get("GRAPROES")),
			GRAPROES_F=safe_float(row.get("GRAPROES_F")),
			GRAPROES_M=safe_float(row.get("GRAPROES_M")),
			RECUCALL_C=safe_int(row.get("RECUCALL_C")),
			RAMPAS_C=safe_int(row.get("RAMPAS_C")),
			PASOPEAT_C=safe_int(row.get("PASOPEAT_C")),
			BANQUETA_C=safe_int(row.get("BANQUETA_C")),
			GUARNICI_C=safe_int(row.get("GUARNICI_C")),
			CICLOVIA_C=safe_int(row.get("CICLOVIA_C")),
			CICLOCAR_C=safe_int(row.get("CICLOCAR_C")),
			ALUMPUB_C=safe_int(row.get("ALUMPUB_C")),
			LETRERO_C=safe_int(row.get("LETRERO_C")),
			TELPUB_C=safe_int(row.get("TELPUB_C")),
			ARBOLES_C=safe_int(row.get("ARBOLES_C")),
			DRENAJEP_C=safe_int(row.get("DRENAJEP_C")),
			TRANSCOL_C=safe_int(row.get("TRANSCOL_C")),
			ACESOPER_C=safe_int(row.get("ACESOPER_C")),
			ACESOAUT_C=safe_int(row.get("ACESOAUT_C")),
		)

		batch.append((record, idx, f"lat={lat}, lon={lon}, POBTOT={pobtot}"))

		if len(batch) >= BATCH_SIZE:
			loaded += commit_batch(db, batch, errors, "UrbanQuality")
			LOGGER.info("UrbanQuality cargados: %d", loaded)
			batch.clear()

	# Persist remaining rows
	loaded += commit_batch(db, batch, errors, "UrbanQuality")

	error_path = error_dir / "errores_urban_quality.txt"
	log_error_summary("Urban Quality", errors, error_path)

	return loaded, skipped


def load_unequality_indicators(df: DataFrame, db: Session, error_dir: Path) -> Tuple[int, int]:
	"""Persist Unequality Indicators rows into the database."""

	required_columns = {"cve_ent", "cve_mun", "Pob_2010", "cve_sun", "cvegeo", "sun"}
	missing_cols = required_columns - set(df.columns)
	if missing_cols:
		raise ValueError(
			"El archivo de Unequality Indicators no contiene las columnas obligatorias: "
			f"{missing_cols}"
		)

	loaded, skipped = 0, 0
	errors = []

	batch: list[Tuple[UnequalityIndicators, int, str]] = []

	for idx, row in df.iterrows():
		cve_ent = safe_int(row.get("cve_ent"))
		cve_mun = safe_int(row.get("cve_mun"))
		pob_2010 = safe_int(row.get("Pob_2010"))
		cve_sun = safe_str(row.get("cve_sun"))
		cvegeo = safe_str(row.get("cvegeo"))
		sun = safe_str(row.get("sun"))

		if None in {cve_ent, cve_mun, pob_2010} or not all([cve_sun, cvegeo, sun]):
			skipped += 1
			continue

		record = UnequalityIndicators(
			cve_ent=cve_ent,
			cve_mun=cve_mun,
			cve_sun=cve_sun or "",
			cvegeo=cvegeo or "",
			sun=sun or "",
			gmu=safe_str(row.get("gmu")),
			iisu_sun=safe_str(row.get("iisu_sun")),
			iisu_cd=safe_str(row.get("iisu_cd")),
			POBTOT=pob_2010,
			Empleo=safe_int(row.get("Empleo")),
			E_basica=safe_int(row.get("E_basica")),
			E_media=safe_int(row.get("E_media")),
			E_superior=safe_int(row.get("E_superior")),
			Salud_cama=safe_int(row.get("Salud_cama")),
			Salud_cons=safe_int(row.get("Salud_cons")),
			Abasto=safe_int(row.get("Abasto")),
			Espacio_ab=safe_int(row.get("Espacio_ab")),
			Cultura=safe_int(row.get("Cultura")),
			Est_Tpte=safe_int(row.get("Est_Tpte")),
			geometry_wkt=safe_str(row.get("geometry")),
			lat=safe_float(row.get("lat")),
			lon=safe_float(row.get("lon")),
		)

		batch.append((record, idx, f"cvegeo={cvegeo}, sun={sun}"))

		if len(batch) >= BATCH_SIZE:
			loaded += commit_batch(db, batch, errors, "UnequalityIndicators")
			LOGGER.info("UnequalityIndicators cargados: %d", loaded)
			batch.clear()

	loaded += commit_batch(db, batch, errors, "UnequalityIndicators")

	error_path = error_dir / "errores_unequality_indicators.txt"
	log_error_summary("Unequality Indicators", errors, error_path)

	return loaded, skipped


def run_import(
	dataset: str,
	base_dir: Path,
	urban_file: Optional[Path],
	unequality_file: Optional[Path],
) -> None:
	"""Run the ETL flow for the chosen dataset(s)."""

	datasets = []
	if dataset in {"urban", "all"}:
		path = urban_file or base_dir / "data_inegi.xlsx"
		datasets.append(("Urban Quality", path, load_urban_quality))
	if dataset in {"unequality", "all"}:
		path = unequality_file or base_dir / "Inequality-MTY.xlsx"
		datasets.append(("Unequality Indicators", path, load_unequality_indicators))

	if not datasets:
		raise ValueError("No se seleccionó ningún dataset para cargar.")

	session = SessionLocal()
	try:
		for label, path, loader in datasets:
			if not path.exists():
				LOGGER.error("Archivo no encontrado para %s: %s", label, path)
				continue

			LOGGER.info("\n%s\n%s\n%s", "=" * 72, f"CARGANDO: {label}", "=" * 72)
			df = read_excel(path)
			loaded, skipped = loader(df, session, base_dir)
			LOGGER.info(
				"Resumen %s -> cargados: %d | saltados: %d",
				label,
				loaded,
				skipped,
			)
	finally:
		session.close()


def build_parser() -> argparse.ArgumentParser:
	"""CLI argument parser."""

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"--dataset",
		choices=["urban", "unequality", "all"],
		default="all",
		help="Define qué dataset cargar (urban, unequality o all).",
	)
	parser.add_argument(
		"--base-dir",
		type=Path,
		default=DEFAULT_STATIC_DIR,
		help="Directorio base donde se ubican los archivos Excel (por defecto: static/).",
	)
	parser.add_argument(
		"--urban-file",
		type=Path,
		help="Ruta explícita al archivo de Urban Quality (sobrescribe base-dir).",
	)
	parser.add_argument(
		"--unequality-file",
		type=Path,
		help="Ruta explícita al archivo de Unequality Indicators (sobrescribe base-dir).",
	)
	parser.add_argument(
		"--verbose",
		action="store_true",
		help="Habilita logs detallados para depuración.",
	)
	return parser


def main(argv: Optional[Iterable[str]] = None) -> None:
	"""Script entrypoint."""

	parser = build_parser()
	args = parser.parse_args(list(argv) if argv is not None else None)
	configure_logging(verbose=args.verbose)

	LOGGER.info("Directorio base: %s", args.base_dir)
	run_import(
		dataset=args.dataset,
		base_dir=args.base_dir,
		urban_file=args.urban_file,
		unequality_file=args.unequality_file,
	)


if __name__ == "__main__":  # pragma: no cover - manual execution entrypoint
	main()