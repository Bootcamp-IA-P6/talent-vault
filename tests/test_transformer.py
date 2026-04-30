import pytest
from src.processing.transformer import parse_salary, parse_sex


# ─── parse_salary ─────────────────────────────────────

def test_parse_salary_euro():
    assert parse_salary("45000€") == "45000"

def test_parse_salary_dollar():
    assert parse_salary("120000$") == "120000"

def test_parse_salary_rupee():
    assert parse_salary("151770₨") == "151770"

def test_parse_salary_no_symbol():
    assert parse_salary("75000") == "75000"

def test_parse_salary_none():
    assert parse_salary(None) is None

def test_parse_salary_empty():
    assert parse_salary("") is None


# ─── parse_sex ────────────────────────────────────────

def test_parse_sex_female():
    assert parse_sex(["F"]) == "F"

def test_parse_sex_male():
    assert parse_sex(["M"]) == "M"

def test_parse_sex_nd():
    assert parse_sex(["ND"]) == "ND"

def test_parse_sex_none():
    assert parse_sex(None) is None

def test_parse_sex_empty_list():
    assert parse_sex([]) is None

def test_parse_sex_string():
    # si por algún motivo llega como string en vez de lista
    assert parse_sex("F") is None