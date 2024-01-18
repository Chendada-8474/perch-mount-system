from datetime import datetime
from sqlalchemy.orm import Session
from service import db_engine
from src.model import Sections, SectionOperators


def get_sections(
    perch_mount: int = None,
    check_date_from: datetime = None,
    check_date_to: datetime = None,
    valid: bool = None,
    operator: int = None,
) -> list[Sections]:
    with Session(db_engine) as session:
        query = session.query(Sections)

        if perch_mount:
            query = query.filter(Sections.perch_mount == perch_mount)

        if check_date_from:
            query = query.filter(Sections.check_date >= check_date_from)

        if check_date_to:
            query = query.filter(Sections.check_date < check_date_to)

        if valid is not None:
            query = query.filter(Sections.valid == valid)

        if operator:
            section_indice = _get_section_indice_by_operator(operator)
            query = query.filter(Sections.section_id.in_(section_indice))

        results = query.all()
    return results


def _get_section_indice_by_operator(member_id: int) -> list[int]:
    with Session(db_engine) as session:
        results = (
            session.query(SectionOperators.section)
            .filter(SectionOperators.operator == member_id)
            .all()
        )
        return [row.section for row in results]


def get_section_by_id(section_id: int) -> Sections:
    with Session(db_engine) as session:
        result = session.query(Sections).filter(Sections.section_id == section_id).one()
    return result


def add_section(
    perch_mount: int,
    mount_type: int,
    camera: int,
    start_time: datetime,
    end_time: datetime,
    valid: bool,
    operators: list[int],
    note: str,
) -> Sections:
    new_section = Sections(
        perch_mount=perch_mount,
        mount_type=mount_type,
        camera=camera,
        start_time=start_time,
        end_time=end_time,
        valid=valid,
        note=note,
    )

    with Session(db_engine) as session:
        try:
            session.add(new_section)
            session.flush()
            section_id = new_section.section_id
            new_section_operators = []
            for operator in operators:
                new_section_operators.append(
                    SectionOperators(
                        section=section_id,
                        operator=operator,
                    )
                )
            session.add_all(new_section_operators)
            session.commit()
        except Exception as e:
            session.rollback()
            raise

    return new_section
