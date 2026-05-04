import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent.parent.parent / ".env")

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def create_table():
    """Crea la tabla de personas si no existe."""
    sql = """
    CREATE TABLE IF NOT EXISTS persons (
        id              SERIAL PRIMARY KEY,
        passport        VARCHAR(20) UNIQUE,
        name            VARCHAR(100),
        last_name       VARCHAR(100),
        sex             VARCHAR(5),
        telfnumber      VARCHAR(50),
        email           VARCHAR(150),
        fullname        VARCHAR(200),
        city            VARCHAR(100),
        address         TEXT,
        company         VARCHAR(200),
        company_address TEXT,
        company_phone   VARCHAR(50),
        company_email   VARCHAR(150),
        job             VARCHAR(150),
        iban            VARCHAR(50),
        salary          VARCHAR(30),
        ipv4            VARCHAR(20),
        created_at      TIMESTAMP DEFAULT NOW()
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

def upsert_person(person: dict):
    """Inserta o actualiza un registro de persona por passport."""
    sql = """
    INSERT INTO persons (
        passport, name, last_name, sex, telfnumber, email,
        fullname, city, address,
        company, company_address, company_phone, company_email, job,
        iban, salary, ipv4
    ) VALUES (
        %(passport)s, %(name)s, %(last_name)s, %(sex)s, %(telfnumber)s, %(email)s,
        %(fullname)s, %(city)s, %(address)s,
        %(company)s, %(company_address)s, %(company_phone)s, %(company_email)s, %(job)s,
        %(iban)s, %(salary)s, %(ipv4)s
    )
    ON CONFLICT (passport) DO UPDATE SET
        name            = EXCLUDED.name,
        last_name       = EXCLUDED.last_name,
        sex             = EXCLUDED.sex,
        telfnumber      = EXCLUDED.telfnumber,
        email           = EXCLUDED.email,
        fullname        = EXCLUDED.fullname,
        city            = EXCLUDED.city,
        address         = EXCLUDED.address,
        company         = EXCLUDED.company,
        company_address = EXCLUDED.company_address,
        company_phone   = EXCLUDED.company_phone,
        company_email   = EXCLUDED.company_email,
        job             = EXCLUDED.job,
        iban            = EXCLUDED.iban,
        salary          = EXCLUDED.salary,
        ipv4            = EXCLUDED.ipv4;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, person)
        conn.commit()