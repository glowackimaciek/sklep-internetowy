from fastapi import APIRouter
from db import conn, cursor
from pydantic import BaseModel

router = APIRouter(prefix="/kategorie", tags=["kategorie"])


class Kategoria(BaseModel):
    nazwa: str


@router.get("/")
def pobierz_kategorie():
    cursor.execute("SELECT * FROM kategorie")
    kategorie = cursor.fetchall()
    return [{"id": k[0], "nazwa": k[1]} for k in kategorie]


@router.post("/")
def dodaj_kategorie(kategoria: Kategoria):
    cursor.execute("INSERT INTO kategorie (nazwa) VALUES (?)", (kategoria.nazwa,))
    conn.commit()
    return {"message": f"Dodano kategorie: {kategoria.nazwa}"}
