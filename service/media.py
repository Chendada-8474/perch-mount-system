from sqlalchemy.orm import Query

import service
from service import utils
from service import query_utils
from src import model


def get_media(
    section_id: int = None,
    perch_mount_id: int = None,
    taxon_order: int = None,
    category: str = None,
    order: str = None,
    family: str = None,
    prey: bool = None,
    offset: int = 0,
    limit: int = 50,
) -> list[model.Media]:
    with service.session.begin() as session:
        query = session.query(
            model.Media.medium_id,
            model.Media.medium_datetime,
            model.Media.section,
            model.Media.path,
            model.Media.empty_checker,
            model.Media.reviewer,
            model.Media.event,
            model.Media.featured_behavior,
            model.Media.featured_by,
            model.Media.featured_title,
            model.Sections.check_date,
            model.PerchMounts.perch_mount_id,
            model.PerchMounts.perch_mount_name,
            model.Projects.name.label("project_name"),
        )

        if section_id:
            query = query.filter(model.Media.section == section_id)

        if perch_mount_id:
            section_indices = query_utils.get_section_indice_by_perch_mount_id(
                perch_mount_id
            )
            query = query.filter(model.Media.section.in_(section_indices))

        query = _filter_media_query_by_individual_conditions(
            query,
            taxon_order=taxon_order,
            category=category,
            order=order,
            family=family,
            prey=prey,
        )

        query = query.join(
            model.Sections,
            model.Sections.section_id == model.Media.section,
        )
        query = query.join(
            model.PerchMounts,
            model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
        )
        query = query.join(
            model.Projects,
            model.Projects.project_id == model.PerchMounts.project,
        )

        query = query.order_by(model.Media.medium_datetime)
        query = query.offset(offset).limit(limit)
        results = query.all()

    return results


def _filter_media_query_by_individual_conditions(
    query: Query[model.Media],
    taxon_order: int = None,
    category: str = None,
    order: str = None,
    family: str = None,
    prey: bool = None,
) -> Query[model.Media]:
    if taxon_order or category or order or family or prey is not None:
        query = query.join(
            model.Individuals, model.Media.medium_id == model.Individuals.medium
        )
    if taxon_order:
        query = query.filter(model.Individuals.taxon_order_by_human == taxon_order)
    if prey:
        query = query.filter(model.Individuals.prey == prey)

    taxon_orders = _get_taxon_orders_indice_by_taxon(
        category=category,
        order=order,
        family=family,
    )
    if taxon_orders:
        query = query.filter(model.Individuals.taxon_order_by_human.in_(taxon_orders))

    return query


def get_medium_by_id(medium_id: str) -> model.Media:
    with service.session.begin() as session:
        query = session.query(
            model.Media.medium_id,
            model.Media.medium_datetime,
            model.Media.section,
            model.Media.path,
            model.Media.empty_checker,
            model.Media.reviewer,
            model.Media.event,
            model.Media.featured_behavior,
            model.Media.featured_by,
            model.Media.featured_title,
            model.Sections.check_date,
            model.PerchMounts.perch_mount_id,
            model.PerchMounts.perch_mount_name,
            model.Projects.name.label("project_name"),
        ).filter(model.Media.medium_id == medium_id)
        query = query.join(
            model.Sections,
            model.Sections.section_id == model.Media.section,
        )
        query = query.join(
            model.PerchMounts,
            model.PerchMounts.perch_mount_id == model.Sections.perch_mount,
        )
        query = query.join(
            model.Projects,
            model.Projects.project_id == model.PerchMounts.project,
        )
        result = query.one_or_none()

    return result


def update_medium(medium_id: str, arg: dict):
    with service.session.begin() as session:
        session.query(model.Media).filter(model.Media.medium_id == medium_id).update(
            arg
        )
        session.commit()


def add_media_and_individuals(media: list[dict]):
    individauls = _get_individauls_from_media(media)
    media = _pop_media_individual(media)
    new_meida: list[model.Media] = []
    new_individuals: list[model.Individuals] = []
    for medium in media:
        new_meida.append(model.Media(**medium))
    for individual in individauls:
        new_individuals.append(model.Individuals(**individual))

    with service.session.begin() as session:
        try:
            session.add_all(new_meida)
            session.flush()
            session.add_all(new_individuals)
            session.commit()
        except:
            session.rollback()
            raise


def _get_individauls_from_media(media: list[dict]) -> list[dict]:
    individuals = []
    for medium in media:
        for individual in medium["individuals"]:
            individual["medium"] = medium["medium_id"]
            individuals.append(individual)
    return individuals


def _pop_media_individual(media: list[dict]) -> list[dict]:
    for medium in media:
        medium.pop("individuals")
    return media


def _get_taxon_orders_indice_by_taxon(
    category: str = None,
    order: str = None,
    family: str = None,
) -> list[int]:
    if not category and not order and not family:
        return

    with service.session.begin() as session:
        query = session.query(model.Species.taxon_order)
        if category:
            query = query.filter(model.Species.category == category)
        if order:
            query = query.filter(model.Species.order == order)
        if family:
            query = query.filter(model.Species.family_latin_name == family)
        results = query.all()
    return [row.taxon_order for row in results]


def review(media: list[dict]):
    media_with_individuals = query_utils.get_media_with_individuals_and_events(media)
    new_meida, new_individuals = query_utils.media_to_insert_format(
        media_with_individuals
    )
    media_indices = [medium["detected_medium_id"] for medium in media]
    empty_paths = [
        utils.get_detected_medium(medium) for medium in media if medium["individuals"]
    ]
    with service.session.begin() as session:
        try:
            session.query(model.DetectedMedia).filter(
                model.DetectedMedia.detected_medium_id.in_(media_indices)
            ).update({"reviewed": True})
            session.add_all(new_meida)
            session.flush()
            session.add_all(new_individuals)

            utils.post_delete_media_task(empty_paths)
            session.commit()

        except:
            session.rollback()
            raise
