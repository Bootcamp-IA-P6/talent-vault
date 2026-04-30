"""Unit tests for the Redis fragment buffer.

Uses a tiny in-memory fake that implements just the redis methods we touch.
The real redis-py client is not required to run these tests.
"""

import time
from collections import defaultdict

from src.storage import redis_client as rc


class FakeRedis:
    """Minimal subset of redis.Redis for unit testing."""

    def __init__(self):
        self.strings: dict[str, tuple[str, float | None]] = {}
        self.sets: dict[str, set[str]] = defaultdict(set)
        self.set_expiry: dict[str, float | None] = {}

    # ---- helpers ----
    def _alive(self, key: str) -> bool:
        if key in self.strings:
            value, exp = self.strings[key]
            if exp is None or exp > time.time():
                return True
            del self.strings[key]
        return False

    # ---- redis API ----
    def setex(self, key, ttl, value):
        self.strings[key] = (value, time.time() + ttl)

    def get(self, key):
        if self._alive(key):
            return self.strings[key][0]
        return None

    def delete(self, *keys):
        for k in keys:
            self.strings.pop(k, None)
            self.sets.pop(k, None)

    def sadd(self, key, *members):
        self.sets[key].update(members)
        return len(members)

    def srem(self, key, *members):
        if key in self.sets:
            for m in members:
                self.sets[key].discard(m)

    def sinter(self, *keys):
        result = None
        for k in keys:
            current = self.sets.get(k, set())
            result = current.copy() if result is None else result & current
        return result or set()

    def expire(self, key, ttl):
        self.set_expiry[key] = time.time() + ttl

    def pipeline(self):
        return FakePipeline(self)

    def close(self):
        pass


class FakePipeline:
    def __init__(self, fake):
        self.fake = fake
        self.calls: list = []

    def setex(self, *args):
        self.calls.append(("setex", args))
        return self

    def delete(self, *args):
        self.calls.append(("delete", args))
        return self

    def sadd(self, *args):
        self.calls.append(("sadd", args))
        return self

    def srem(self, *args):
        self.calls.append(("srem", args))
        return self

    def expire(self, *args):
        self.calls.append(("expire", args))
        return self

    def execute(self):
        for op, args in self.calls:
            getattr(self.fake, op)(*args)
        self.calls.clear()


# ---- tests ----

def _personal(passport, name, last_name, **extra):
    return {"passport": passport, "name": name, "last_name": last_name,
            "email": "x@y", "telfnumber": "1", "sex": "F", **extra}


def _bank(passport, **extra):
    return {"passport": passport, "IBAN": "IBAN" + passport, "salary": "100", **extra}


def _professional(fullname, **extra):
    return {"fullname": fullname, "company": "Acme", "job": "Dev",
            "company address": "Main 1", "company_email": "a@b",
            "company_telfnumber": "2", **extra}


def _location(fullname, address, **extra):
    return {"fullname": fullname, "city": "Madrid", "address": address, **extra}


def _net(address, ipv4="1.2.3.4"):
    return {"address": address, "IPv4": ipv4}


def test_assemble_returns_none_when_only_personal_buffered():
    fake = FakeRedis()
    rc.register_fragment(fake, "personal", _personal("P1", "Hilda", "Alvarez"), 60)
    person = rc.try_assemble_person(fake, _personal("P1", "Hilda", "Alvarez"))
    assert person is None


def test_assemble_returns_full_person_when_all_five_present():
    fake = FakeRedis()
    rc.register_fragment(fake, "bank", _bank("P1"), 60)
    rc.register_fragment(fake, "professional", _professional("Hilda Alvarez Vergara"), 60)
    rc.register_fragment(fake, "location", _location("Hilda Alvarez", "Calle 1"), 60)
    rc.register_fragment(fake, "net", _net("Calle 1"), 60)

    person = rc.try_assemble_person(fake, _personal("P1", "Hilda", "Alvarez"))

    assert person is not None
    assert person["passport"] == "P1"
    assert person["fullname"] == "Hilda Alvarez"
    assert person["IBAN"] == "IBANP1"
    assert person["company"] == "Acme"
    assert person["city"] == "Madrid"
    assert person["IPv4"] == "1.2.3.4"


def test_assemble_consumes_fragments_so_a_second_attempt_returns_none():
    fake = FakeRedis()
    rc.register_fragment(fake, "bank", _bank("P1"), 60)
    rc.register_fragment(fake, "professional", _professional("Hilda Alvarez"), 60)
    rc.register_fragment(fake, "location", _location("Hilda Alvarez", "Calle 1"), 60)
    rc.register_fragment(fake, "net", _net("Calle 1"), 60)

    first = rc.try_assemble_person(fake, _personal("P1", "Hilda", "Alvarez"))
    second = rc.try_assemble_person(fake, _personal("P1", "Hilda", "Alvarez"))

    assert first is not None
    assert second is None


def test_fuzzy_match_tolerates_extra_tokens_in_fullname():
    fake = FakeRedis()
    rc.register_fragment(fake, "bank", _bank("P9"), 60)
    rc.register_fragment(fake, "professional", _professional("Lic. Hilda Alvarez Vergara"), 60)
    rc.register_fragment(fake, "location", _location("Lic. Hilda Alvarez Vergara", "C9"), 60)
    rc.register_fragment(fake, "net", _net("C9"), 60)

    person = rc.try_assemble_person(fake, _personal("P9", "Hilda", "Alvarez"))

    assert person is not None
    assert person["company"] == "Acme"
    assert person["address"] == "C9"


def test_two_personals_compete_for_same_fullname_one_wins_one_loses():
    """If two distinct personals share name+last_name tokens, only one can claim each professional/location."""
    fake = FakeRedis()
    rc.register_fragment(fake, "bank", _bank("P1"), 60)
    rc.register_fragment(fake, "bank", _bank("P2"), 60)
    rc.register_fragment(fake, "professional", _professional("Hilda Alvarez"), 60)
    rc.register_fragment(fake, "location", _location("Hilda Alvarez", "Addr1"), 60)
    rc.register_fragment(fake, "net", _net("Addr1"), 60)

    first = rc.try_assemble_person(fake, _personal("P1", "Hilda", "Alvarez"))
    second = rc.try_assemble_person(fake, _personal("P2", "Hilda", "Alvarez"))

    assert first is not None
    assert second is None
