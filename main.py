from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr
from typing import List
import uuid
from datetime import datetime, time
import re
import math

app = FastAPI()

# In-memory storage
receipts = {}

class Item(BaseModel):
    shortDescription: constr(pattern=r"^[\w\s\-]+$")
    price: constr(pattern=r"^\d+\.\d{2}$")

class Receipt(BaseModel):
    retailer: constr(pattern=r"^[\w\s\-&]+$")
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: constr(pattern=r"^\d+\.\d{2}$")

def calculate_points(receipt: Receipt) -> int:
    points = 0
    
    # Rule 1: One point for every alphanumeric character in the retailer name
    alphanumeric_count = len([c for c in receipt.retailer if c.isalnum()])
    points += alphanumeric_count
    
    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if receipt.total.endswith('.00'):
        points += 50
    
    # Rule 3: 25 points if the total is a multiple of 0.25
    total_float = float(receipt.total)
    if total_float % 0.25 == 0:
        points += 25
    
    # Rule 4: 5 points for every two items on the receipt
    points += (len(receipt.items) // 2) * 5
    
    # Rule 5: Points for items with descriptions that are multiples of 3
    # Multiply the price by 0.2 and round up
    for item in receipt.items:
        trimmed_desc = item.shortDescription.strip()
        if len(trimmed_desc) % 3 == 0:
            points += math.ceil(float(item.price) * 0.2)
    
    # Rule 6: 6 points if the purchase date is odd
    purchase_date = datetime.strptime(receipt.purchaseDate, '%Y-%m-%d')
    if purchase_date.day % 2 == 1:
        points += 6
    
    # Rule 7: 10 points if the time of purchase is between 2:00pm and 4:00pm
    purchase_time = datetime.strptime(receipt.purchaseTime, '%H:%M').time()
    if time(14, 0) <= purchase_time <= time(16, 0):
        points += 10
    
    return points

@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    try:
        # Validate date format
        datetime.strptime(receipt.purchaseDate, '%Y-%m-%d')
        # Validate time format
        datetime.strptime(receipt.purchaseTime, '%H:%M')
        
        receipt_id = str(uuid.uuid4())
        receipts[receipt_id] = receipt
        return {"id": receipt_id}
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Please verify input. Invalid date or time format."
        )

@app.get("/receipts/{id}/points")
async def get_points(id: str):
    if id not in receipts:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    
    points = calculate_points(receipts[id])
    return {"points": points}