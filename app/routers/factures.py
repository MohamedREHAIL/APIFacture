from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Facture])
def list_factures(db: Session = Depends(get_db)):
    return db.query(models.Facture).all()

@router.post("/", response_model=schemas.Facture)
def create_facture(facture: schemas.FactureCreate, db: Session = Depends(get_db)):
   
    new_facture = models.Facture(
    client_id=facture.client_id,
    date_facturation=date.today(),
    statut=facture.statut,
    iban=facture.iban,
    bic=facture.bic,
    compte_proprietaire=facture.compte_proprietaire,
    banque_domiciliation=facture.banque_domiciliation,
    conditions_reglement=facture.conditions_reglement,
    total_ht=0,
    total_tva=0,
    total_ttc=0
)

    db.add(new_facture)
    db.commit()
    db.refresh(new_facture)

    total_ht = 0
    total_tva = 0

    for ligne in facture.lignes:
        ligne_ht = ligne.prix_unitaire_ht * ligne.quantite
        ligne_tva = ligne_ht * (ligne.taux_tva / 100)

        db_ligne = models.LigneFacture(
            facture_id=new_facture.id,
            designation=ligne.designation,
            prix_unitaire_ht=ligne.prix_unitaire_ht,
            quantite=ligne.quantite,
            taux_tva=ligne.taux_tva,
            total_ht=ligne_ht,
            total_tva=ligne_tva,
        )
        total_ht += ligne_ht
        total_tva += ligne_tva
        db.add(db_ligne)

    total_ttc = total_ht + total_tva
    new_facture.total_ht = total_ht
    new_facture.total_tva = total_tva
    new_facture.total_ttc = total_ttc
    new_facture.statut = "validée"

    db.commit()
    db.refresh(new_facture)

    return new_facture
