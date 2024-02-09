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
