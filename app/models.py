from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    adresse = Column(String, nullable=False)
    code_postal = Column(String, nullable=False)
    ville = Column(String, nullable=False)
    date_creation=Column(Date,nullable=False)
    factures = relationship("Facture", back_populates="client")

class Produit(Base):
    __tablename__ = "produits_catalogue"
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prix_unitaire_ht = Column(Numeric(10, 2), nullable=False)
    tva_historiques = relationship("TVAHistorique", back_populates="produit")

class TVAHistorique(Base):
    __tablename__ = "tva_produit_historique"
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey("produits_catalogue.id"))
    taux = Column(Numeric(4, 2), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=True)
    produit = relationship("Produit", back_populates="tva_historiques")

class Facture(Base):
    __tablename__ = "factures"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    date_facturation = Column(Date, nullable=False)
    statut = Column(String, default="brouillon")
    total_ht = Column(Numeric(10, 2))
    total_tva = Column(Numeric(10, 2))
    total_ttc = Column(Numeric(10, 2))
    iban = Column(String(34))
    bic = Column(String(11))
    compte_proprietaire = Column(String(100))
    banque_domiciliation = Column(String(100))
    conditions_reglement = Column(String(100), nullable=False)
    client = relationship("Client", back_populates="factures")
    lignes = relationship("LigneFacture", back_populates="facture")

class LigneFacture(Base):
    __tablename__ = "facture_lignes"
    id = Column(Integer, primary_key=True)
    facture_id = Column(Integer, ForeignKey("factures.id"))
    designation = Column(String, nullable=False)
    prix_unitaire_ht = Column(Numeric(10, 2))
    quantite = Column(Integer)
    taux_tva = Column(Numeric(4, 2))
    total_ht = Column(Numeric(10, 2))
    total_tva = Column(Numeric(10, 2))
    facture = relationship("Facture", back_populates="lignes")
