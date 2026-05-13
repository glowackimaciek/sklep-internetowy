from fastapi import APIRouter
from db import conn, cursor
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/produkty", tags=["produkty"])


class Produkt(BaseModel):
    nazwa: str
    cena: float
    opis: str
    ilosc: int
    kategoria_id: Optional[int] = None


@router.get("/")
def pobierz_produkty():
    cursor.execute("SELECT * FROM produkty")
    produkty = cursor.fetchall()
    return [
        {
            "id": p[0],
            "nazwa": p[1],
            "cena": p[2],
            "opis": p[3],
            "ilosc": p[4],
            "kategoria": p[5],
        }
        for p in produkty
    ]


@router.post("/")
def dodaj_produkt(produkt: Produkt):
    cursor.execute(
        "INSERT INTO produkty (nazwa, cena, opis, ilosc, kategoria_id) VALUES (?, ?, ?, ?, ?)",
        (
            produkt.nazwa,
            produkt.cena,
            produkt.opis,
            produkt.ilosc,
            produkt.kategoria_id,
        ),
    )
    conn.commit()
    return {"message": f"Dodano produkt: {produkt.nazwa}"}
