import service
import typing
from src import model


ID_COLUMN_TABLE = {"medium": "medium_id", "detected_medium": "detected_medium_id"}


def get_section_indice_by_perch_mount_id(perch_mount_id: int) -> list[int]:
    with service.session.begin() as session:
        results = (
            session.query(model.Sections.section_id)
            .filter(model.Sections.perch_mount == perch_mount_id)
            .all()
        )
    return [row.section_id for row in results]


def get_individauls_from_detected_media(media: list[dict]) -> list[dict]:
    individuals = []
    id_field = "medium_id" if "medium_id" in media[0] else "detected_medium_id"

    for medium in media:
        for individual in medium["individuals"]:
            individual["medium"] = medium[id_field]
            individuals.append(individual)
    return individuals


def pop_media_individual(media: list[dict]) -> list[dict]:
    for medium in media:
        medium.pop("individuals")
    return media


def meida_to_insert_format(media: list[dict]) -> tuple[list, list]:
    individauls = get_individauls_from_detected_media(media)
    media = pop_media_individual(media)
    new_meida: list[model.DetectedMedia] = []
    new_individuals: list[model.DetectedIndividuals] = []
    for medium in media:
        new_meida.append(model.DetectedMedia(**medium))
    for individual in individauls:
        new_individuals.append(model.DetectedIndividuals(**individual))
    return new_meida, new_individuals


def find_section_operators(
    section_id: int, operators: list[int]
) -> list[model.SectionOperators]:
    section_operators = [
        model.SectionOperators(section=section_id, operator=operator)
        for operator in operators
    ]
    return section_operators
