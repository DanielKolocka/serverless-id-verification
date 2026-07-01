# Serverless ID Verification API

Mock identity verification API built with AWS serverless services as a learning project.

## Architecture
```
Client → API Gateway → Lambda → DynamoDB
```

## Endpoints

**POST /verify**
Use Postman to send a POST request to `https://xxx.execute-api.ca-central-1.amazonaws.com/verify/f9155f4d-2033-4847-b989-d4310579e` with a JSON body:
```json
{"id_number": "ABC123XY", "country_code": "CA"}
```
- `id_number` — alphanumeric, 8-12 uppercase characters
- `country_code` — 2 uppercase letters (e.g. `CA`, `US`)

**GET /verify/{requestID}**
Send a GET request in Postman to `https://xxx.execute-api.ca-central-1.amazonaws.com/verify/YOUR_REQUEST_ID`

## AWS Services
- **Lambda** — Python 3.14, handles validation and DynamoDB reads/writes
- **API Gateway** — HTTP API exposing POST and GET routes
- **DynamoDB** — stores results with `requestID` as partition key
- **IAM** — least-privilege role scoped to `PutItem`/`GetItem` on the table

## Deploy
Deployed via the AWS Lambda console by uploading a zipped function package.
