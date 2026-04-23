from src.processing.transformer import (
    build_person,
    index_by,
    index_by_fullname_tokens,
    pop_fuzzy_match,
    pop_match,
)


def test_index_by_groups_items_by_key():
    items = [{"passport": "A", "v": 1}, {"passport": "B", "v": 2}, {"passport": "A", "v": 3}]
    result = index_by(items, "passport")
    assert len(result["A"]) == 2
    assert len(result["B"]) == 1


def test_index_by_skips_missing_key():
    items = [{"passport": "A"}, {"other": "X"}]
    result = index_by(items, "passport")
    assert "A" in result
    assert len(result) == 1


def test_pop_match_consumes_once():
    index = {"A": [{"v": 1}, {"v": 2}]}
    first = pop_match(index, "A")
    second = pop_match(index, "A")
    third = pop_match(index, "A")
    assert first == {"v": 1}
    assert second == {"v": 2}
    assert third == {}


def test_pop_match_returns_empty_for_missing_key():
    assert pop_match({"A": [{"v": 1}]}, "B") == {}
    assert pop_match({}, None) == {}


def test_index_by_fullname_tokens_creates_entry_per_word():
    items = [{"fullname": "Hilda Alvarez Vergara"}]
    index = index_by_fullname_tokens(items)
    assert items[0] in index["Hilda"]
    assert items[0] in index["Alvarez"]
    assert items[0] in index["Vergara"]


def test_pop_fuzzy_match_finds_record_with_extra_tokens():
    records = [
        {"fullname": "Hilda Alvarez Vergara", "city": "Madrid"},
        {"fullname": "Nelly Alvarez", "city": "Barcelona"},
    ]
    index = index_by_fullname_tokens(records)
    match = pop_fuzzy_match(index, "Hilda", "Alvarez")
    assert match["city"] == "Madrid"


def test_pop_fuzzy_match_consumes_so_next_call_returns_different():
    records = [
        {"fullname": "Hilda Alvarez", "city": "Madrid"},
        {"fullname": "Hilda Alvarez", "city": "Barcelona"},
    ]
    index = index_by_fullname_tokens(records)
    first = pop_fuzzy_match(index, "Hilda", "Alvarez")
    second = pop_fuzzy_match(index, "Hilda", "Alvarez")
    third = pop_fuzzy_match(index, "Hilda", "Alvarez")
    cities = {first["city"], second["city"]}
    assert cities == {"Madrid", "Barcelona"}
    assert third == {}


def test_pop_fuzzy_match_returns_empty_when_no_match():
    index = index_by_fullname_tokens([{"fullname": "Nelly Alvarez"}])
    assert pop_fuzzy_match(index, "Hilda", "Alvarez") == {}


def test_pop_fuzzy_match_returns_empty_for_missing_inputs():
    index = index_by_fullname_tokens([{"fullname": "Hilda Alvarez"}])
    assert pop_fuzzy_match(index, None, "Alvarez") == {}
    assert pop_fuzzy_match(index, "Hilda", None) == {}


def test_build_person_joins_all_five_types():
    personal = {
        "name": "Hilda",
        "last_name": "Alvarez",
        "passport": "V46577426",
        "email": "h@x.com",
        "telfnumber": "+34 111",
        "sex": ["F"],
    }
    bank_index = {"V46577426": [{"IBAN": "ES123", "salary": "50000€"}]}
    prof_index = index_by_fullname_tokens([
        {"fullname": "Hilda Alvarez Vergara", "company": "ACME", "job": "Engineer"},
    ])
    loc_index = index_by_fullname_tokens([
        {"fullname": "Hilda Alvarez Vergara", "city": "Santa Rosa", "address": "Av 1"},
    ])
    net_index = {"Av 1": [{"IPv4": "1.2.3.4"}]}

    person = build_person(personal, bank_index, prof_index, loc_index, net_index)

    assert person is not None
    assert person["passport"] == "V46577426"
    assert person["fullname"] == "Hilda Alvarez"
    assert person["sex"] == "F"
    assert person["IBAN"] == "ES123"
    assert person["company"] == "ACME"
    assert person["city"] == "Santa Rosa"
    assert person["IPv4"] == "1.2.3.4"


def test_build_person_returns_none_when_no_passport():
    assert build_person({"name": "X"}, {}, {}, {}, {}) is None


def test_build_person_fills_nulls_for_missing_fragments():
    personal = {"name": "Solo", "last_name": "Lonely", "passport": "P1"}
    person = build_person(personal, {}, {}, {}, {})
    assert person is not None
    assert person["passport"] == "P1"
    assert person["IBAN"] is None
    assert person["company"] is None
    assert person["city"] is None
    assert person["IPv4"] is None
