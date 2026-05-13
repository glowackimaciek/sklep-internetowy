from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import produkty, kategorie, koszyk, zamowienia

app = FastAPI(title="Sklep internetowy")

app.include_router(produkty.router)
app.include_router(kategorie.router)
app.include_router(koszyk.router)
app.include_router(zamowienia.router)

@app.get("/")
def root():
    return {"message": "Witaj w sklepie"}


