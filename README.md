# Formation Software Inginner

Projet de formation en programmation et développement logiciel.

## Présentation

Cette application propose une API REST simple pour gérer des produits avec FastAPI. Elle comprend :
- un modèle Produit
- une couche service
- un dépôt avec persistance SQLite
- des endpoints Swagger accessibles via FastAPI
- des tests automatisés avec pytest

## Technologies utilisées

- Python
- FastAPI
- Uvicorn
- SQLite
- pytest

## Installation

Créer et activer l’environnement virtuel :

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install -r requirements.txt
```

## Lancer l’API

```powershell
uvicorn app.api.main_api:app --reload
```

L’interface Swagger sera disponible sur :
- http://127.0.0.1:8000/docs

## Lancer l’interface web Streamlit

```powershell
streamlit run app/ui/streamlit_app.py
```

L’interface web sera disponible sur :
- http://localhost:8501

## Exécuter les tests

```powershell
pytest -q
```