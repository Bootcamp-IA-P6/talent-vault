from src.consumer.kafka_consumer import (
    BANK,
    LOCATION,
    NET,
    PERSONAL,
    PROFESSIONAL,
    UNKNOWN,
    classify,
)


def test_classify_personal():
    payload = {
        "name": "Elladio",
        "last_name": "Trombetta",
        "sex": ["M"],
        "telfnumber": "+34 123 456 789",
        "passport": "243641523",
        "email": "vincent45@club-internet.fr",
    }
    assert classify(payload) == PERSONAL


def test_classify_bank():
    payload = {
        "passport": "243641523",
        "IBAN": "GB69CWZE0751701352026",
        "salary": "183258€",
    }
    assert classify(payload) == BANK


def test_classify_professional():
    payload = {
        "fullname": "Elladio Trombetta",
        "company": "Laboratorios León y Espinosa",
        "company address": "Avenida Norte 798",
        "company_telfnumber": "+34 823 166 908",
        "company_email": "catalina53@casas-zavala.info",
        "job": "Conserje",
    }
    assert classify(payload) == PROFESSIONAL


def test_classify_location():
    payload = {
        "fullname": "Elladio Trombetta",
        "city": "Merlo",
        "address": "Camino Corrientes N° 9770",
    }
    assert classify(payload) == LOCATION


def test_classify_net():
    payload = {"address": "Camino Corrientes N° 9770", "IPv4": "69.167.76.189"}
    assert classify(payload) == NET


def test_classify_unknown_empty():
    assert classify({}) == UNKNOWN


def test_classify_unknown_partial():
    assert classify({"email": "x@y.com"}) == UNKNOWN


def test_classify_location_not_confused_with_net():
    loc = {"fullname": "X Y", "city": "Madrid", "address": "calle 1"}
    assert classify(loc) == LOCATION
    net = {"address": "calle 1", "IPv4": "1.2.3.4"}
    assert classify(net) == NET
