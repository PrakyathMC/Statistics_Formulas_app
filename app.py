import uvicorn
from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Load data
with open("statistics_formulas.json", 'r') as f:
    formulas = json.load(f)

# Add CORS middleware to allow requests from any origin
# This is fine for development, but for production, specify the origins you want to allow
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, for development only!
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# an endpoint to list all formulas:
# an endpoint to list all formulas:
@app.get("/formulas")
async def get_all_formulas():
    return [{"name": formula["formula_name"], "id": index} for index, formula in enumerate(formulas)]

# endpoint to get details for a specific formula:
@app.get("/formula/{formula_id}")
async def get_formula(formula_id: int):
    if formula_id < 0 or formula_id >= len(formulas):
        raise HTTPException(status_code=404, detail="Formula not found")
    return formulas[formula_id]

@app.get("/search")
async def search_formulas(query: str):
    return [formula for formula in formulas if query.lower() in formula["formula_name"].lower()]



# Run the API with uvicorn
# Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

# uvicorn app:app --reload