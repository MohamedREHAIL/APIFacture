from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import app.schemas as schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.TVAHistorique])
def list_tva(db: Session = Depends(get_db)):
    return db.query(models.TVAHistorique).all()

@router.post("/", response_model=schemas.TVAHistorique)
def create_tva(tva: schemas.TVAHistoriqueCreate, db: Session = Depends(get_db)):
    db_tva = models.TVAHistorique(**tva.dict())
    db.add(db_tva)
    db.commit()
    db.refresh(db_tva)
    return db_tva
