def classify(msg: dict) -> str:
    if "sex"     in msg: return "personal_data"
    if "city"    in msg: return "location"
    if "company" in msg: return "professional_data"
    if "IBAN"    in msg: return "bank_data"
    if "IPv4"    in msg: return "net_data"
    return "unknown"