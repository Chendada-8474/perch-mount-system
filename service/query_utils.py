import service
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


def get_individauls_from_media(media: list[dict]) -> list[dict]:
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


def _fit_model_medium(medium: dict) -> model.Media:
    return model.Media(
        medium_id=medium["detected_medium_id"],
        section=medium["section"],
        medium_datetime=medium["medium_datetime"],
        path=medium["path"],
        empty_checker=(medium["empty_checker"] if "empty_checker" in medium else None),
        reviewer=medium["reviewer"],
        event=medium["event"] if "event" in medium else None,
        featured=medium["featured"] if "featured" in medium else None,
        featured_by=medium["featured_by"] if "featured_by" in medium else None,
        featured_title=(
            medium["featured_title"] if "featured_title" in medium else None
        ),
        featured_behavior=(
            medium["featured_behavior"] if "featured_behavior" in medium else None
        ),
    )


def _fit_model_individual(individual: dict) -> model.Individuals:
    return model.Individuals(
        taxon_order_by_ai=(
            individual["taxon_order_by_ai"]
            if "taxon_order_by_ai" in individual
            else None
        ),
        taxon_order_by_human=individual["taxon_order_by_human"],
        medium=individual["medium"],
        prey=individual["prey"] if "prey" in individual else None,
        prey_name=individual["prey_name"] if "prey_name" in individual else None,
        tagged=individual["tagged"] if "tagged" in individual else False,
        ring_number=individual["ring_number"] if "ring_number" in individual else None,
        xmin=individual["xmin"] if "xmin" in individual else None,
        xmax=individual["xmax"] if "xmax" in individual else None,
        ymin=individual["ymin"] if "ymin" in individual else None,
        ymax=individual["ymax"] if "ymax" in individual else None,
    )


def media_to_insert_format(media: list[dict]):
    individuals = get_individauls_from_media(media)
    media = pop_media_individual(media)
    new_media: list[model.Media] = []
    new_individuals: list[model.Individuals] = []
    for medium in media:
        new_medium = _fit_model_medium(medium)
        new_media.append(new_medium)
    for individual in individuals:
        new_individual = _fit_model_individual(individual)
        new_individuals.append(new_individual)
    return new_media, new_individuals


def detected_meida_to_insert_format(
    media: list[dict], section: int
) -> tuple[list, list]:
    individauls = get_individauls_from_media(media)
    media = pop_media_individual(media)
    new_meida: list[model.DetectedMedia] = []
    new_individuals: list[model.DetectedIndividuals] = []
    for medium in media:
        medium["section"] = section
        new_meida.append(model.DetectedMedia(**medium))
    for individual in individauls:
        new_individuals.append(model.DetectedIndividuals(**individual))
    return new_meida, new_individuals


def empty_media_to_insert_format(media: list[dict], section) -> list[model.EmptyMedia]:
    new_media: list[model.EmptyMedia] = []

    for medium in media:
        medium["section"] = section
        new_media.append(model.EmptyMedia(**medium))

    return new_media


def find_section_operators(
    section_id: int, operators: list[int]
) -> list[model.SectionOperators]:
    section_operators = [
        model.SectionOperators(section=section_id, operator=operator)
        for operator in operators
    ]
    return section_operators


def get_media_with_individuals_and_events(media: list[dict]) -> list[dict]:
    new_media = []
    for medium in media:
        if medium["individuals"] or medium["event"]:
            new_media.append(medium)
    return new_media
