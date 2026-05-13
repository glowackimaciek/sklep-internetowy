from fastapi import APIRouter
from db import conn, cursor
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/zamowienia", tags=["zamowienia"])


@router.post("/{sesja_id}")
def zloz_zamowienie(sesja_id: str):
    # pobierz koszyk
    cursor.execute(
        """
        SELECT k.produkt_id, k.ilosc, p.cena
        FROM koszyk k
        JOIN produkty p ON k.produkt_id = p.id
        WHERE k.sesja_id = ?
    """,
        (sesja_id,),
    )
    koszyk = cursor.fetchall()

    if not koszyk:
        return {"error": "Koszyk jest pusty"}

    # policz sume
    suma = sum(p[1] * p[2] for p in koszyk)

    # stwórz zamówienie
    cursor.execute(
        "INSERT INTO zamowienia (data, status, suma) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), "nowe", suma),
    )
    zamowienie_id = cursor.lastrowid

    # dodaj pozycje zamowienia
    for pozycja in koszyk:
        cursor.execute(
            "INSERT INTO pozycje_zamowienia (zamowienie_id, produkt_id, ilosc, cena) VALUES (?, ?, ?, ?)",
            (zamowienie_id, pozycja[0], pozycja[1], pozycja[2]),
        )

    # wyczysc koszyk
    cursor.execute("DELETE FROM koszyk WHERE sesja_id = ?", (sesja_id,))
    conn.commit()

    return {"message": f"Zamówienie #{zamowienie_id} złożone!", "suma": suma}
