# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="АСКУ API", description="Бэкенд для системы кадрового учета")

class CompanyCreate(BaseModel):
    name: str
    inn: Optional[str] = None
    address: Optional[str] = None

fake_db_companies = []

@app.post("/api/companies/", tags=["Компании"])
async def create_company(company: CompanyCreate):
    # Проверка на дубликаты ИНН
    for c in fake_db_companies:
        if c["inn"] == company.inn:
            raise HTTPException(status_code=400, detail="Компания с таким ИНН уже существует")
    
    new_company = {
        "id": len(fake_db_companies) + 1,
        "name": company.name,
        "inn": company.inn,
        "address": company.address
    }
    fake_db_companies.append(new_company)
    return {"message": "Компания успешно создана", "data": new_company}

@app.get("/api/companies/", tags=["Компании"])
async def get_companies():
    """Получение списка всех компаний"""
    return fake_db_companies

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
