from fastapi import APIRouter, HTTPException, Query
from src.storage.sql_client import get_connection

router = APIRouter(prefix="/persons", tags=["Persons"])


def fetch_all(sql: str, params: tuple = ()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            cols = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
    return [dict(zip(cols, row)) for row in rows]


def fetch_one(sql: str, params: tuple = ()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            cols = [desc[0] for desc in cur.description]
            row  = cur.fetchone()
    if not row:
        return None
    return dict(zip(cols, row))


# ─── Endpoints ────────────────────────────────────────

@router.get("/")
def list_persons(
    limit:  int = Query(20, ge=1, le=200, description="Número de resultados"),
    offset: int = Query(0,  ge=0,          description="Desplazamiento")
):
    """Lista paginada de personas."""
    rows = fetch_all(
        "SELECT * FROM persons ORDER BY id LIMIT %s OFFSET %s",
        (limit, offset)
    )
    return {"total": len(rows), "limit": limit, "offset": offset, "data": rows}


@router.get("/search")
def search_persons(
    name:    str = Query(None, description="Buscar por nombre o apellido"),
    city:    str = Query(None, description="Buscar por ciudad"),
    company: str = Query(None, description="Buscar por empresa"),
    job:     str = Query(None, description="Buscar por puesto")
):
    """Búsqueda flexible por nombre, ciudad, empresa o puesto."""
    filters, params = [], []

    if name:
        filters.append("(name ILIKE %s OR last_name ILIKE %s)")
        params += [f"%{name}%", f"%{name}%"]
    if city:
        filters.append("city ILIKE %s")
        params.append(f"%{city}%")
    if company:
        filters.append("company ILIKE %s")
        params.append(f"%{company}%")
    if job:
        filters.append("job ILIKE %s")
        params.append(f"%{job}%")

    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    rows  = fetch_all(f"SELECT * FROM persons {where} LIMIT 100", tuple(params))
    return {"total": len(rows), "data": rows}


@router.get("/stats")
def stats():
    """Estadísticas generales de la base de datos."""
    total     = fetch_one("SELECT COUNT(*) AS total FROM persons")
    by_sex    = fetch_all("SELECT sex, COUNT(*) AS count FROM persons GROUP BY sex ORDER BY count DESC")
    top_cities = fetch_all("SELECT city, COUNT(*) AS count FROM persons GROUP BY city ORDER BY count DESC LIMIT 5")
    top_jobs  = fetch_all("SELECT job, COUNT(*) AS count FROM persons GROUP BY job ORDER BY count DESC LIMIT 5")

    return {
        "total_persons": total["total"],
        "by_sex":        by_sex,
        "top_cities":    top_cities,
        "top_jobs":      top_jobs
    }


@router.get("/{passport}")
def get_person(passport: str):
    """Obtiene el perfil completo de una persona por su passport."""
    person = fetch_one("SELECT * FROM persons WHERE passport = %s", (passport,))
    if not person:
        raise HTTPException(status_code=404, detail=f"Persona con passport '{passport}' no encontrada")
    return person