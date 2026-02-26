# Projet 5 - Industrialisation Modèle ML (Turnover Employé)

## Description
Pipeline de Machine Learning industriel pour prédire le départ des employés (`a_quitte_l_entreprise`).
Le projet inclut le prétraitement des données, l'entraînement du modèle, une API de prédiction, une base de données PostgreSQL et une pipeline CI/CD.

## Installation

### Prérequis
- Python 3.8+
- Git
- PostgreSQL (pour l'étape 4)

### Procédure
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/votre-user/ocrproject5.git
   cd ocrproject5
   ```

2. Créer un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Entraînement du modèle
Pour lancer le pipeline d'entraînement et sauvegarder le modèle :
```bash
python src/model.py
```
Le modèle est sauvegardé dans `models/model.pkl`.

### Tests
Pour lancer la suite de tests unitaires et fonctionnels :
```bash
pytest tests/ --cov=src
```

### API (À venir)
Pour lancer le serveur API (après développement étape 3) :
```bash
uvicorn src.api:app --reload
```

## Structure du Projet

ocrproject5/
├── src/
│   ├── __init__.py
│   ├── data.py          # Chargement et fusion des données
│   ├── preprocessing.py # Pipelines de transformation
│   └── model.py         # Entraînement et sauvegarde
├── tests/               # Tests unitaires et fonctionnels
├── data/                # Données brutes (ignoré par .gitignore)
├── models/              # Modèles sérialisés (.pkl)
├── docs/                # Documentation technique
├── .github/workflows/   # Pipeline CI/CD
├── .gitignore
├── requirements.txt
└── README.md

