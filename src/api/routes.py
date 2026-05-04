from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from src.api.dependencies import get_session
from src.models.sql_models import Person

router = APIRouter()


@router.get("/persons")
def list_persons(
    city: str | None = Query(None),
    company: str | None = Query(None),
    search: str | None = Query(
        None,
        description="Substring match on passport, name, last_name, fullname or email (case-insensitive)",
    ),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
) -> dict:
    stmt = select(Person)
    if city:
        stmt = stmt.where(Person.city == city)
    if company:
        stmt = stmt.where(Person.company == company)
    if search:
        like = f"%{search}%"
        stmt = stmt.where(
            Person.passport.ilike(like)
            | Person.name.ilike(like)
            | Person.last_name.ilike(like)
            | Person.fullname.ilike(like)
            | Person.email.ilike(like)
        )

    total = session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = session.scalars(stmt.limit(limit).offset(offset)).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [_serialize(p) for p in rows],
    }


@router.get("/persons/{passport}")
def get_person(passport: str, session: Session = Depends(get_session)) -> dict:
    person = session.get(Person, passport)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return _serialize(person)


@router.get("/stats")
def stats(session: Session = Depends(get_session)) -> dict:
    total = session.scalar(select(func.count()).select_from(Person)) or 0

    by_city = session.execute(
        select(Person.city, func.count().label("c"))
        .where(Person.city.is_not(None))
        .group_by(Person.city)
        .order_by(desc("c"))
        .limit(10)
    ).all()

    by_company = session.execute(
        select(Person.company, func.count().label("c"))
        .where(Person.company.is_not(None))
        .group_by(Person.company)
        .order_by(desc("c"))
        .limit(10)
    ).all()

    by_job = session.execute(
        select(Person.job, func.count().label("c"))
        .where(Person.job.is_not(None))
        .group_by(Person.job)
        .order_by(desc("c"))
        .limit(10)
    ).all()

    by_sex = session.execute(
        select(Person.sex, func.count().label("c"))
        .where(Person.sex.is_not(None))
        .group_by(Person.sex)
        .order_by(desc("c"))
    ).all()

    return {
        "total_persons": total,
        "top_cities": [{"city": c, "count": n} for c, n in by_city],
        "top_companies": [{"company": c, "count": n} for c, n in by_company],
        "top_jobs": [{"job": j, "count": n} for j, n in by_job],
        "sex_distribution": [{"sex": s, "count": n} for s, n in by_sex],
    }


def _serialize(person: Person) -> dict:
    return {
        "passport": person.passport,
        "name": person.name,
        "last_name": person.last_name,
        "fullname": person.fullname,
        "email": person.email,
        "telfnumber": person.telfnumber,
        "sex": person.sex,
        "IBAN": person.IBAN,
        "salary": person.salary,
        "company": person.company,
        "company_address": person.company_address,
        "company_email": person.company_email,
        "company_telfnumber": person.company_telfnumber,
        "job": person.job,
        "city": person.city,
        "address": person.address,
        "IPv4": person.IPv4,
    }
