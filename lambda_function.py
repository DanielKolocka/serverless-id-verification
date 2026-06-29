import re
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VerificationResults')

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

def lambda_handler(event, context):
    print('Event:', event)
    body = event.get('body', {})
    id_number = body.get('id_number')
    country_code = body.get('country_code')

    print(f'Validating ID: {id_number} for country: {country_code}')
    