import service
from src import model


def get_section_indice_by_perch_mount_id(perch_mount_id: int) -> list[int]:
    with service.session.begin() as session:
        results = (
            session.query(model.Sections.section_id)
            .filter(model.Sections.perch_mount == perch_mount_id)
            .all()
        )
    return [row.section_id for row in results]


def get_individauls_from_media(media: list[dict]) -> list[dict]:
    individuals = []
    for medium in media:
        for individual in medium["individuals"]:
            individual["medium"] = medium["medium_id"]
            individuals.append(individual)
    return individuals


def pop_media_individual(media: list[dict]) -> list[dict]:
    for medium in media:
        medium.pop("individuals")
    return media


def meida_to_insert_format(
    detected_media: list[dict],
) -> (
    list[model.Media] | list[model.DetectedMedia],
    list[model.Individuals] | list[model.DetectedIndividuals],
):
    individauls = get_individauls_from_media(detected_media)
    detected_media = pop_media_individual(detected_media)
    new_meida: list[model.DetectedMedia] = []
    new_individuals: list[model.DetectedIndividuals] = []
    for medium in detected_media:
        new_meida.append(model.DetectedMedia(**medium))
    for individual in individauls:
        new_individuals.append(model.DetectedIndividuals(**individual))
    return new_meida, new_individuals
