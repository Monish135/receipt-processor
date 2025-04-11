# Receipt Processor

A REST API service that processes receipts and calculates points based on specific rules.

## Overview

This service provides two endpoints:
- Process receipts and returns a unique ID
- Retrieve points for a processed receipt using its ID

The points are calculated based on the following rules:
1. One point for every alphanumeric character in the retailer name
2. 50 points if the total is a round dollar amount with no cents
3. 25 points if the total is a multiple of 0.25
4. 5 points for every two items on the receipt
5. If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer for points
6. 6 points if the day in the purchase date is odd
7. 10 points if the time of purchase is between 2:00pm and 4:00pm

## Technical Stack

- Python 3.12
- FastAPI
- Docker
- Pydantic for data validation
- Uvicorn ASGI server

## Getting Started

### Prerequisites

- Docker and Docker Compose
  OR
- Python 3.12+

### Running with Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Monish135/receipt-processor
cd receipt-processor
```

2. Build and run the Docker container:
```bash
docker-compose up --build
```

The service will be available at `http://localhost:8000`

### Running Locally

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

### Process Receipt

**Endpoint:** POST /receipts/process

**Request Body:**
```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    }
  ],
  "total": "6.49"
}
```

**Response:**
```json
{
  "id": "adb6b560-0eef-42bc-9d16-df48f30e89b2"
}
```

### Get Points

**Endpoint:** GET /receipts/{id}/points

**Response:**
```json
{
  "points": 32
}
```

## Testing

You can test the API using curl:

```bash
# Process a receipt
curl -X POST -H "Content-Type: application/json" -d '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    }
  ],
  "total": "6.49"
}' http://localhost:8000/receipts/process

# Get points (replace {id} with the ID returned from the process endpoint)
curl http://localhost:8000/receipts/{id}/points
```

## Data Persistence

The application uses in-memory storage, so data will not persist when the application is stopped or restarted.

## API Specification

The API follows the OpenAPI 3.0.3 specification. You can view the complete API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Successful operation
- 400: Invalid input (with "Please verify input." message)
- 404: Receipt ID not found

## Project Structure

