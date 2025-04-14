from typing import List
from pydantic import BaseModel
from datetime import date


# === CLIENT ===
class ClientCreate(BaseModel):
    nom: str
    adresse: str
    code_postal: str
    ville: str
    date_creation: date


class Client(ClientCreate):
    id: int
    class Config:
        from_attributes = True

# === PRODUIT ===
class ProduitCreate(BaseModel):
    nom: str
    prix_unitaire_ht: float

class Produit(ProduitCreate):
    id: int
    class Config:
        from_attributes = True

# === TVA ===
class TVAHistoriqueCreate(BaseModel):
    produit_id: int
    taux: float
    date_debut: date
    date_fin: date | None = None


class TVAHistorique(TVAHistoriqueCreate):
    id: int
    class Config:
        from_attributes = True

# LIGNES DE FACTURE
class LigneFactureBase(BaseModel):
    designation: str
    prix_unitaire_ht: float
    quantite: int
    taux_tva: float

class LigneFactureCreate(LigneFactureBase):
    pass

class LigneFactureOut(LigneFactureBase):
    id: int
    total_ht: float
    total_tva: float

    class Config:
        from_attributes = True

# === FACTURE ===
class FactureCreate(BaseModel):
    client_id: int
    statut: str
    iban: str
    bic: str
    compte_proprietaire: str
    banque_domiciliation: str
    conditions_reglement: str
    lignes: List[LigneFactureCreate]

class Facture(BaseModel):
    id: int
    client_id: int
    date_facturation: date
    statut: str
    total_ht: float
    total_tva: float
    total_ttc: float
    iban: str
    bic: str
    compte_proprietaire: str
    banque_domiciliation: str
    conditions_reglement: str
    lignes: List[LigneFactureOut]

    class Config:
        from_attributes = True


