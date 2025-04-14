from fastapi import FastAPI
from app.routers import clients, produits, tva, factures
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Facturation Okayo")

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API Okayo"}


app.include_router(clients.router, prefix="/clients", tags=["Clients"])
app.include_router(produits.router, prefix="/produits", tags=["Produits"])
app.include_router(tva.router, prefix="/tva", tags=["TVA"])
app.include_router(factures.router, prefix="/factures", tags=["Factures"])

