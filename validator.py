import re


def validate_id(id_number: str, country_code: str) -> dict:
    errors = []

    if not re.match(r'^[A-Z0-9]{8,12}$', id_number):
        errors.append("Invalid ID format. It should be alphanumeric and 8-12 characters long.")

    if not re.match(r'^[A-Z]{2}$', country_code):
        errors.append("Invalid country code format. It should be two uppercase letters.")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

print(validate_id("ABC123XY", "CA"))   # valid
print(validate_id("123", "ca"))        # invalid — too short, lowercase country
print(validate_id("VALIDID99", "US"))  # valid
print(validate_id("VALIDID", "US"))    # invalid - too short
print(validate_id("VALIDID99", "us"))    # invalid - lowercase country

