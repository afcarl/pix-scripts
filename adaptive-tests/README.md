# Tests adaptatifs dans PIX

## Prérequis

    brew install python3

Optionnel :

    brew install pypy3  # Accélérer la génération des tests adaptatifs
    brew install graphviz  # Pour afficher un test adaptatif (peu profond) sous forme de graphe

## Installation

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## Génération

- Télécharger les épreuves au format CSV depuis la vue JJV dans AirTable, les mettre dans `data`.
- `python epreuves.py` crée `epreuves<id>.json` et `prerequis<id>.json`.
- `pypy3 dummy.py <nb_questions>` crée un test adaptatif de profondeur au plus `<nb_questions>` et l'enregistre au format JSON (`scenarios<id>.json`, 2 min de cuisson environ sur un MBA i5 1.3 GHz mid-2013).
- `python json2csv.py` crée l'équivalent `scenarios<id>.csv`.
- `python airtable.py` permet de mettre à jour le test dans Airtable avec les bonnes épreuves.

## Simulation

(optionnel : `pip install Flask`)

`python3 cat.py 20` permet de simuler le test adaptatif avec une interface en Flask.

## Installation dans une review app

    mv data/scenarios.csv data/<scenarios_file>
    scp data/<scenarios_file> <pix@pix>:placement_tests
    ssh <pix@pix>
    pix placement_tests:load <app_name> <scenarios_file>

## Mise en production

Dans une base `pg_staging` en local, importer les scénarios de la façon suivante :

    psql pg_staging
    # \copy scenarios("courseId",path,"nextChallengeId") from '/path/to/scenarios.csv' delimiter ',' csv

Ensuite vous pourrez exporter seulement la table `scenarios` :

    pg_dump --data-only --table=scenarios pg_staging > scenarios.dump

Pour ensuite l'importer sur le serveur PIX :

    dokku postgres:connect pg-staging < scenarios.dump

(Attention, `pg-staging` (avec un dash) est le nom de l'application Dokku, tandis que `pg_staging` (avec un underscore) est le nom de la base de données.)
