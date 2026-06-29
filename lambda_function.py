import re
import uuid
import boto3
from datetime import datetime, timezone


dynamodb = boto3.resource('dynamodb')
myTable = dynamodb.Table('VerificationResults')

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
    try:   
        print('Event:', event)
        body = event.get('body', {})
        id_number = body.get('id_number')
        country_code = body.get('country_code')

        print(f'Validating ID: {id_number} for country: {country_code}')

        if not id_number or not country_code:
            return {
                'statusCode': 400,
                'body': {
                    'message': 'id_number and country_code are required.'
                }
            }
        
        result = validate_id(id_number, country_code)

        # Build the record to store in DB
        request_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.pst).isoformat()

        record = {
            'request_id': request_id,
            'id_number': id_number,
            'country_code': country_code,
            'is_valid': result['is_valid'],
            'errors': result['errors'],
            'timestamp': timestamp
        }

        myTable.put_item(Item=record)

        return {
            'statusCode': 200,
            'body': {
                'request_id': request_id,
                'is_valid': result['is_valid'],
                'errors': result['errors'],
                'timestamp': timestamp
            }
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': {
                'error': str(e)
            }
        }