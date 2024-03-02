from collections import defaultdict

from src.model import (
    SectionOperators,
    Individuals,
    DetectedIndividuals,
    DetectedMedia,
    Species,
)


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
    medium_key = (
        media[0]["medium_id"] if "medium_id" in media[0] else "detected_medium_id"
    )
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


def get_indiivduals_taxon_orders(individuals: list[DetectedIndividuals]) -> list[int]:
    return [sp.taxon_order_by_ai for sp in individuals]
