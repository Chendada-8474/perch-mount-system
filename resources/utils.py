from collections import defaultdict
import flask
import cache.key

from src.model import SectionOperators


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
