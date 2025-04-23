# Data Analyzer

Un outil d'analyse de données qui traite les fichiers CSV, effectue des analyses statistiques et génère des visualisations à l'aide de Pandas, Matplotlib et Seaborn.

## Installation

### Prérequis
- Python 3.6 ou supérieur

### Étapes d'installation

1. Clonez le répertoire :
   ```
   git clone <votre-url-git>
   cd data-analyzer
   ```

2. Créez un environnement virtuel (Windows) :
   ```
   python -m venv venv
   ```

3. Activez l'environnement virtuel :
   - Windows (Invite de commandes) :
     ```
     venv\Scripts\activate.bat
     ```
   - Windows (PowerShell) - si vous rencontrez des erreurs de politique d'exécution :
     ```
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     venv\Scripts\Activate.ps1
     ```
   - Linux/macOS :
     ```
     source venv/bin/activate
     ```

4. Installez les dépendances :
   ```
   pip install -e .
   ```

## Structure du projet

```
data-analyzer/
├── data/                # Répertoire contenant les fichiers de données CSV
├── src/                 # Code source principal
│   ├── __init__.py
│   ├── data_loader.py   # Module pour charger et prétraiter les données
│   ├── analyzer.py      # Module pour l'analyse des données
│   └── visualizer.py    # Module pour la visualisation des données
├── tests/               # Tests unitaires
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_analyzer.py
│   └── test_visualizer.py
├── main.py              # Point d'entrée principal de l'application
├── setup.py             # Script d'installation
└── README.md            # Ce fichier
```

## Utilisation

### Interface en ligne de commande

L'application fournit une interface en ligne de commande pour analyser et visualiser des données CSV :

```
python main.py [fichier_csv] [options]
```

#### Options d'analyse

- `--analysis`, `-a` : Type d'analyse à effectuer (choix : summary, time-series, distribution, top-categories, customer-segments, customer-metrics, correlation)
- `--groupby`, `-g` : Colonne pour le regroupement
- `--n-top`, `-n` : Nombre d'éléments principaux à afficher
- `--frequency`, `-f` : Fréquence pour l'analyse des séries temporelles (D, W, M, Q, Y)
- `--start-date` : Date de début pour le filtrage (YYYY-MM-DD)
- `--end-date` : Date de fin pour le filtrage (YYYY-MM-DD)
- `--category` : Filtrer par catégorie
- `--customer` : Filtrer par ID client

#### Options de visualisation

- `--plot`, `-p` : Type de graphique à créer (choix : bar, line, pie, heatmap, histogram, box, scatter)
- `--x-column` : Colonne pour l'axe X dans le nuage de points
- `--y-column` : Colonne pour l'axe Y dans le nuage de points
- `--title` : Titre du graphique
- `--xlabel` : Étiquette pour l'axe X
- `--ylabel` : Étiquette pour l'axe Y
- `--color` : Couleur du graphique
- `--horizontal` : Créer un graphique à barres horizontal
- `--figsize` : Taille de la figure en pouces (largeur,hauteur)

#### Options de sortie

- `--output`, `-o` : Répertoire pour enregistrer les fichiers de sortie
- `--format` : Format pour sauvegarder les graphiques (png, jpg, svg, pdf)
- `--dpi` : DPI pour sauvegarder les graphiques
- `--no-display` : Ne pas afficher les graphiques, seulement les sauvegarder

### Exemples d'utilisation

1. Afficher un résumé statistique des données :
   ```
   python main.py data/sample_data.csv --analysis summary
   ```

2. Créer un graphique à barres des catégories les plus dépensées :
   ```
   python main.py data/sample_data.csv --analysis top-categories --plot bar --output results
   ```

3. Analyser les tendances de dépenses sur une période spécifique :
   ```
   python main.py data/sample_data.csv --analysis time-series --start-date 2023-01-15 --end-date 2023-02-15 --plot line
   ```

4. Créer un diagramme circulaire de la distribution des dépenses par catégorie :
   ```
   python main.py data/sample_data.csv --analysis distribution --plot pie --output results
   ```

## Exécution des tests

Pour exécuter les tests unitaires :

```
pytest
```

Pour exécuter un module de test spécifique :

```
pytest tests/test_data_loader.py
```

## Fonctionnalités

- Chargement et validation des données CSV
- Filtrage des données par date, catégorie et client
- Statistiques descriptives avec regroupement optionnel
- Analyse de séries temporelles avec différentes fréquences
- Segmentation des clients basée sur les modèles de dépenses
- Visualisations diverses : graphiques à barres, à lignes, circulaires, cartes thermiques, histogrammes, boîtes à moustaches et nuages de points
- Personnalisation des graphiques (titres, étiquettes, couleurs, etc.)
- Enregistrement des visualisations dans différents formats