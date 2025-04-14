
# 🧾 Première partie Modèle de Données (Fichier APIFacture.drawio.png)

## 🎯 Objectifs Fonctionnels

L'application de gestion de factures doit permettre :

- La création, la consultation et le suivi des factures clients.
- L’évolution continue des prestations proposées via un catalogue centralisé.
- L’application de taux de TVA historiques par produit et par période.
- L’archivage immuable des factures émises, garantissant que les montants (HT, TVA, TTC) ne changent jamais après validation.

---

## 🧱 Architecture de Données

### Entités Principales

| Table                  | Rôle                                                                 |
|------------------------|----------------------------------------------------------------------|
| `clients`              | Référentiel des clients facturés                                     |
| `produits_catalogue`   | Liste des prestations proposées (avec nom, prix HT)                  |
| `tva_produit_historique` | Historique des taux de TVA par produit avec périodes de validité     |
| `factures`             | Informations principales sur chaque facture                          |
| `facture_lignes`       | Détail des lignes de facture, incluant une copie des données du produit et de la TVA au moment de la facturation |

---

### 🔗 Relations et Cardinalités

```
clients (1) ───────< factures (1) ───────< facture_lignes

produits_catalogue (1) ───────< tva_produit_historique
```

> 🔐 Il n’y a pas de relation directe entre `facture_lignes` et `produits_catalogue` : les données sont copiées pour rester figées dans les lignes de facture.

---

### 🔐 Figer les Données de Facturation

Une facture doit toujours refléter l’état du catalogue et des taux de TVA au moment de son émission. C’est pourquoi, lors de la création d’une facture :

- Le nom du produit (désignation)
- Le prix HT unitaire
- Le taux de TVA applicable

... sont copiés dans la table `facture_lignes` et ne dépendent plus de l’état futur du catalogue ou des taux de TVA.

---

### 📆 Gestion de la TVA dans le Temps

La table `tva_produit_historique` permet de suivre les variations de TVA par produit. Elle comprend pour chaque produit :

- Un taux applicable (ex : 20%, 5.5%, etc.)
- Une période de validité (`date_debut`, `date_fin`)

```sql
SELECT taux
FROM tva_produit_historique
WHERE produit_id = :produit_id
  AND :date_facture BETWEEN date_debut AND COALESCE(date_fin, '9999-12-31');
```

Cela permet de garantir que le bon taux de TVA est appliqué au bon moment.

---



## 🧾 Exemple de Génération de Facture (Workflow Simplifié)

1. L'utilisateur sélectionne un client.
2. Il choisit des prestations dans le catalogue.
3. Pour chaque prestation :
   - Le système récupère le prix HT courant.
   - Il détermine le taux de TVA applicable à la date de facturation.
   - Il copie tous ces éléments dans `facture_lignes`.
4. Les totaux HT, TVA et TTC sont calculés et enregistrés dans la table `factures`.
5. La facture passe en statut **validée** → elle devient **immuable**.

---

#  Deuxième partie : Guide de Lancement – API Facture (code source)

## 1. Prérequis

Avant toute chose, assurez-vous d’avoir les outils suivants installés sur votre machine :

- **Docker** (et Docker Compose) : pour exécuter l’API et la base de données dans des conteneurs isolés sans configuration manuelle.
- **Facultatif** : un outil comme **Postman** ou **cURL** pour tester les routes API (Swagger UI est déjà intégré).

---

## 2. Lancer l’application

### Cloner le dépôt Git

```bash
git clone https://github.com/votre-utilisateur/APIFacture.git
cd APIFacture
```

### Lancer le projet avec Docker

```bash
docker-compose up --build
```

Patientez quelques secondes que les services soient prêts, puis ouvrez votre navigateur à l’adresse suivante :

📎 [http://localhost:8000/docs](http://localhost:8000/docs)  
👉 Accès à la documentation interactive de l’API (Swagger UI)

---

## 🧱 Architecture du Projet

L'application suit une architecture claire et modulaire, reposant sur :

- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**

### 📁 `app/`

Contient le cœur de l’application.

#### 📄 `main.py`
- Point d’entrée de l’API FastAPI.
- Configure l’instance FastAPI.
- Monte les routes des modules : clients, produits, tva, factures.
- Configure Swagger UI.

#### 📄 `database.py`
- Définit la chaîne de connexion PostgreSQL (via `.env`).
- Crée la session de base (SessionLocal) pour les opérations CRUD.
- Fournit une dépendance injectable pour gérer proprement les sessions DB.

#### 📄 `models.py`
Contient tous les modèles SQLAlchemy représentant les entités :

- **Client** : infos client (nom, adresse, date, etc.)
- **Produit** : prestations/services offerts.
- **TVAHistorique** : taux de TVA par période.
- **Facture** : infos de facturation (totaux HT/TVA/TTC, coordonnées, etc.)
- **LigneFacture** : lignes détaillées d’une facture.

Les relations entre tables sont gérées avec `relationship` et `ForeignKey`.

#### 📄 `schemas.py`
Contient les schémas **Pydantic** utilisés pour :

- **Valider** les données entrantes (POST, PUT, PATCH).
- **Structurer** les réponses API.

Exemples :
- `FactureCreate`, `FactureOut`
- `ClientBase`, `TVAHistoriqueBase`

Sépare les rôles de validation et de réponse.

#### 📁 `routers/`
Regroupe les routes API par entité :

- `clients.py` → `/clients/` : gestion des clients.
- `produits.py` → `/produits/` : gestion des produits/prestations.
- `tva.py` → `/tva/` : gestion des taux de TVA.
- `factures.py` → `/factures/` : création de factures, calculs HT/TVA/TTC.

Chaque route :
- Valide les requêtes avec les schémas.
- Interagit avec la base via SQLAlchemy.
- Retourne une réponse formatée.

---

### 🐳 Fichiers Docker

#### 📄 `Dockerfile`
- Utilise l’image `python:3.12`
- Copie les fichiers, installe les dépendances.
- Lance l’application avec `uvicorn`.

#### 📄 `docker-compose.yml`
- Définit deux services :
  - `web` : application FastAPI.
  - `db` : base PostgreSQL 15.
- Configure le réseau et monte les ports.

---

## 🔄 Interactions entre Fichiers

1. L’utilisateur fait une requête via Swagger UI ou Postman.
2. FastAPI route la requête vers le bon fichier dans `routers/`.
3. Les données sont validées avec Pydantic.
4. Une session DB est ouverte via `get_db()` de `database.py`.
5. L’opération est réalisée avec les modèles SQLAlchemy.
6. La réponse formatée est renvoyée.

---


