import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^(\+91[\-\s]?|0)?[6-9]\d{9}$'
    return re.match(pattern,phone) is not None
