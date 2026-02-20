# API de Prédiction de Turnover

Projet 5 OpenClassrooms - Mise en production d'un modèle de Machine Learning.

## Description

Ce projet expose un modèle de prédiction de turnover d'employés via une API.
Le modèle a été entraîné dans le cadre du Projet 4 et est maintenant industrialisé.

## Structure du projet

- `src/model/` : Code du modèle et du preprocessing
- `src/api/` : API FastAPI ou Flask (à venir)
- `src/database/` : Gestion PostgreSQL (à venir)
- `tests/` : Tests unitaires et fonctionnels (à venir)
- `.github/workflows/` : CI/CD avec GitHub Actions (à venir)

## Installation

```bash
# Cloner le repo
git clone https://github.com/Breizhux/ocrproject5.git
cd ocrproject5

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## Modèle

Le modèle de prédiction de turnover utilise une régression logistique.
