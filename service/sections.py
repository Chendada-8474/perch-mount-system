from datetime import datetime, date

import service
from src import model


def get_sections(
    perch_mount: int = None,
    check_date_from: datetime = None,
    check_date_to: datetime = None,
    valid: bool = None,
    operator: int = None,
) -> list[model.Sections]:
    with service.session.begin() as session:
        query = session.query(model.Sections)

        if perch_mount:
            query = query.filter(model.Sections.perch_mount == perch_mount)

        if check_date_from:
            query = query.filter(model.Sections.check_date >= check_date_from)

        if check_date_to:
            query = query.filter(model.Sections.check_date < check_date_to)

        if valid is not None:
            query = query.filter(model.Sections.valid == valid)

        if operator:
            query = query.join(
                model.SectionOperators,
                model.SectionOperators.section == model.Sections.section_id,
            ).filter(model.SectionOperators.operator == operator)

        results = query.all()
    return results


def get_section_operators(section_indice: list[int]) -> list[model.SectionOperators]:
    with service.session.begin() as session:
        results = (
            session.query(model.SectionOperators)
            .filter(model.SectionOperators.section.in_(section_indice))
            .all()
        )
    return result


def get_section_by_id(section_id: int) -> model.Sections:
    with service.session.begin() as session:
        result = (
            session.query(model.Sections)
            .filter(model.Sections.section_id == section_id)
            .one()
        )
    return result


def add_section(
    perch_mount: int,
    mount_type: int,
    camera: int,
    start_time: datetime,
    end_time: datetime,
    check_date: date,
    valid: bool,
    operators: list[int],
    note: str,
) -> int:
    new_section = model.Sections(
        perch_mount=perch_mount,
        mount_type=mount_type,
        camera=camera,
        start_time=start_time,
        end_time=end_time,
        check_date=check_date,
        valid=valid,
        note=note,
    )

    with service.session.begin() as session:
        try:
            session.add(new_section)
            session.flush()
            section_id = new_section.section_id
            new_section_operators = []
            for operator in operators:
                new_section_operators.append(
                    model.SectionOperators(
                        section=section_id,
                        operator=operator,
                    )
                )
            session.add_all(new_section_operators)
            session.commit()

            new_id = new_section.section_id
        except Exception as e:
            session.rollback()
            raise

    return new_id
