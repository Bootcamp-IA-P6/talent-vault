from src.storage.mongo_client import get_db
from src.storage.sql_client import upsert_person, create_table
from src.utils.logger import logger
from src.monitoring.metrics import (
    PERSONS_PROCESSED,
    PERSONS_SKIPPED,
    TRANSFORMER_DURATION,
)
import time
import re


def parse_salary(salary_str: str) -> str:
    """Limpia el salary: '45000€' → '45000'"""
    if not salary_str:
        return None
    return re.sub(r"[^\d]", "", salary_str) or None


def parse_sex(sex_val) -> str:
    """Normaliza sex: ['F'] → 'F', None → None"""
    if isinstance(sex_val, list) and sex_val:
        return sex_val[0]
    return None


def build_person(passport: str, db) -> dict | None:
    personal = db["personal_data"].find_one({"passport": passport})
    bank     = db["bank_data"].find_one({"passport": passport})

    if not personal or not bank:
        logger.debug(f"passport={passport} — falta personal o bank, omitido")
        return None

    fullname = (personal.get("name", "") + " " + personal.get("last_name", "")).strip()

    location     = db["location"].find_one({"fullname": {"$regex": fullname, "$options": "i"}})
    professional = db["professional_data"].find_one({"fullname": {"$regex": fullname, "$options": "i"}})
    net          = db["net_data"].find_one({"address": location.get("address")}) if location else None

    return {
        "passport":        passport,
        "name":            personal.get("name"),
        "last_name":       personal.get("last_name"),
        "sex":             parse_sex(personal.get("sex")),
        "telfnumber":      personal.get("telfnumber"),
        "email":           personal.get("email"),
        "fullname":        location.get("fullname")            if location     else fullname,
        "city":            location.get("city")                if location     else None,
        "address":         location.get("address")             if location     else None,
        "company":         professional.get("company")         if professional else None,
        "company_address": professional.get("company address") if professional else None,
        "company_phone":   professional.get("company_telfnumber") if professional else None,
        "company_email":   professional.get("company_email")   if professional else None,
        "job":             professional.get("job")             if professional else None,
        "iban":            bank.get("IBAN"),
        "salary":          parse_salary(bank.get("salary")),
        "ipv4":            net.get("IPv4") if net else None,
    }


def run_transformer():
    db = get_db()
    create_table()

    passports = db["personal_data"].distinct("passport")
    total     = len(passports)
    logger.info(f"Iniciando procesamiento de {total} personas")

    start = time.time()
    ok, skipped = 0, 0

    for passport in passports:
        person = build_person(passport, db)
        if person:
            upsert_person(person)
            ok += 1
            PERSONS_PROCESSED.inc()
            logger.info(f"passport={passport} | {person.get('name')} {person.get('last_name')} → insertado")
        else:
            skipped += 1
            PERSONS_SKIPPED.inc()
            logger.warning(f"passport={passport} → datos incompletos, omitido")

    duration = time.time() - start
    TRANSFORMER_DURATION.observe(duration)
    logger.info(f"Completado: {ok} insertados | {skipped} omitidos | {total} totales | duration={duration:.2f}s")


if __name__ == "__main__":
    run_transformer()