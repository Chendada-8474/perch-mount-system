import base64
from collections import defaultdict
from datetime import datetime, date
import pathlib
import urllib.parse

from src.model import (
    SectionOperators,
    Individuals,
    DetectedIndividuals,
    DetectedMedia,
    Species,
)

import src.config


def get_habitat_indice(resources: list) -> list[int]:
    return list(set(row.habitat for row in resources))


def get_claimer_indice(resources: list) -> list[int]:
    return list(set(row.claim_by for row in resources))


def get_project_indice(resources: list) -> list[int]:
    return list(set(row.project for row in resources))


def get_nodup_values(resources: list[dict], field: str) -> list:
    return list(set(row[field] for row in resources))


def field_as_key(resources: list[dict], field: str) -> dict[int, dict]:
    table = {}
    for row in resources:
        table[row[field]] = row
        row.pop(field)
    return table


def find_section_operator_map(
    section_operators: list[SectionOperators],
) -> dict[int, int]:
    mapping = defaultdict(list)
    for row in section_operators:
        mapping[row.section].append(row.operator)
    return mapping


def _medium_id_as_key(individuals: list[dict]) -> dict:
    medium_key_individuals = defaultdict(list)
    for individual in individuals:
        medium_id = individual["medium"]
        individual.pop("medium")
        medium_key_individuals[medium_id].append(individual)
    return medium_key_individuals


def embed_individuals_to_media(media: dict, individuals: dict) -> list[dict]:
    if not media:
        return []
    media_key_individuals = _medium_id_as_key(individuals)
    medium_key = "medium_id" if "medium_id" in media[0] else "detected_medium_id"
    for medium in media:
        medium["individuals"] = media_key_individuals[medium[medium_key]]
    return media


def taxon_order_as_key(species: list[Species]) -> dict[int, dict]:
    key_species = {}
    for sp in species:
        d = sp.to_json()
        key = d["taxon_order"]
        d.pop("taxon_order")
        key_species[key] = d
    return key_species


def get_indiivduals_taxon_orders(individuals: list) -> list[int]:
    taxon_orders = []
    for individual in individuals:
        taxon_orders.append(individual.taxon_order_by_ai)
        if hasattr(individual, "taxon_order_by_human"):
            taxon_orders.append(individual.taxon_order_by_human)
    return taxon_orders


def to_dict(result) -> dict:
    new_result: dict = result._asdict()
    for k, v in new_result.items():
        if type(v) == datetime or type(v) == date:
            new_result[k] = v.isoformat()
    return new_result


def custom_results_to_dict(results) -> list[dict]:
    return [to_dict(result) for result in results]


def add_medium_info(medium: dict) -> dict:
    medium_id_col = _determin_medium_id(medium)
    medium["extension"] = pathlib.Path(medium["path"]).suffix
    medium["is_image"] = medium["extension"][1:].lower() in src.config.IMAGE_EXTENSIONS
    path = str(
        pathlib.PurePath(
            src.config.get_env(src.config.EnvKeys.MINIO_BUCKET),
            medium["project_name"],
            medium["perch_mount_name"],
            medium["check_date"],
            (
                medium[medium_id_col] + "JPEG"
                if medium["is_images"]
                else medium["extension"]
            ),
        )
    )
    medium["s3_path"] = urllib.parse.urljoin(
        src.config.get_env(src.config.EnvKeys.MINIO), path
    )
    medium["base32_path"] = _base32_encode(medium["path"])
    return medium


def add_media_info(media: list[dict]) -> list[dict]:
    new_media = []
    for medium in media:
        new_medium = add_medium_info(medium)
        new_media.append(new_medium)

    return new_media


def _determin_medium_id(medium: dict) -> str:
    DETECTED_MEDIUM_ID_COL = "detected_medium_id"
    EMPTY_MEDIUM_ID_COL = "empty_medium_id"
    MEDIUM_ID_COL = "medium_id"
    if DETECTED_MEDIUM_ID_COL in medium:
        return DETECTED_MEDIUM_ID_COL
    elif EMPTY_MEDIUM_ID_COL in medium:
        return EMPTY_MEDIUM_ID_COL
    else:
        return MEDIUM_ID_COL


def _base32_encode(s: str) -> str:
    return base64.b32encode(s.encode("UTF-8")).decode("UTF-8")
