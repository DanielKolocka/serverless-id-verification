import json
import re
import uuid
import boto3
from datetime import datetime, timezone
from zoneinfo import ZoneInfo



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
        if event.get('requestContext', {}).get('http', {}).get('method') == 'GET':
            request_id = event.get('pathParameters', {}).get('requestID')
            if not request_id:
                return {'statusCode': 400, 'body': json.dumps({'error': 'requestId required'})}
    
            response = myTable.get_item(Key={'requestID': request_id})
            item = response.get('Item')
    
            if not item:
                return {'statusCode': 404, 'body': json.dumps({'error': 'Not found'})}
    
            return {'statusCode': 200, 'body': json.dumps(item, default=str)}  
        print('Event:', event)
        body = json.loads(event.get('body', {}))
        id_number = body.get('id_number')
        country_code = body.get('country_code')

        print(f'Validating ID: {id_number} for country: {country_code}')

        if not id_number or not country_code:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'id_number and country_code are required.'
                })
            }
        
        result = validate_id(id_number, country_code)

        # Build the record to store in DB
        requestID = str(uuid.uuid4())
        print(f'Generated request_id: {requestID}')
        timestamp = datetime.now(ZoneInfo("America/Los_Angeles")).isoformat()

        record = {
            'requestID': requestID,
            'id_number': id_number,
            'country_code': country_code,
            'is_valid': result['is_valid'],
            'errors': result['errors'],
            'timestamp': timestamp
        }

        myTable.put_item(Item=record)

        if not record['is_valid']:
            return {
            'statusCode': 400,
            'body': json.dumps({
                'requestID': requestID,
                'is_valid': result['is_valid'],
                'errors': result['errors'],
                'timestamp': timestamp
            })
        }

        return {
            'statusCode': 200,
            'body': json.dumps({
                'requestID': requestID,
                'is_valid': result['is_valid'],
                'errors': result['errors'],
                'timestamp': timestamp
            })
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

