import pytest
from src.consumer.utils import classify


def test_classify_personal_data():
    msg = {"name": "Nancy", "last_name": "Barnes", "sex": ["F"], "telfnumber": "123", "passport": "A123", "email": "a@b.com"}
    assert classify(msg) == "personal_data"


def test_classify_location():
    msg = {"fullname": "Nancy Barnes", "city": "Madrid", "address": "Calle Mayor 1"}
    assert classify(msg) == "location"


def test_classify_professional_data():
    msg = {"fullname": "Nancy Barnes", "company": "Acme", "company address": "Calle 1", "company_telfnumber": "123", "company_email": "a@acme.com", "job": "Engineer"}
    assert classify(msg) == "professional_data"


def test_classify_bank_data():
    msg = {"passport": "A123", "IBAN": "GB60IBIQ05688362407629", "salary": "45000€"}
    assert classify(msg) == "bank_data"


def test_classify_net_data():
    msg = {"address": "Calle Mayor 1", "IPv4": "192.168.1.1"}
    assert classify(msg) == "net_data"


def test_classify_unknown():
    msg = {"foo": "bar"}
    assert classify(msg) == "unknown"


def test_classify_empty():
    assert classify({}) == "unknown"