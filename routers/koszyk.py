from fastapi import APIRouter
from db import conn, cursor
from pydantic import BaseModel

router = APIRouter(prefix="/koszyk", tags=["koszyk"])


class PozycjaKoszyka(BaseModel):
    produkt_id: int
    ilosc: int
    sesja_id: str


@router.get("/{sesja_id}")
def pobierz_koszyk(sesja_id: str):
    cursor.execute(
        """
        SELECT k.id, p.nazwa, p.cena, k.ilosc
        FROM koszyk k
        JOIN produkty p ON k.produkt_id = p.id
        WHERE k.sesja_id = ?
    """,
        (sesja_id,),
    )
    pozycja = cursor.fetchall()
    return [{"id": p[0], "nazwa": p[1], "cena": p[2], "ilosc": p[3]} for p in pozycja]


@router.post("/")
def dodaj_do_koszyka(pozycja: PozycjaKoszyka):
    cursor.execute(
        "INSERT INTO koszyk (produkt_id, ilosc, sesja_id) VALUES (?, ?, ?)",
        (pozycja.produkt_id, pozycja.ilosc, pozycja.sesja_id),
    )
    conn.commit()
    return {"message": "Dodano do koszyka"}
