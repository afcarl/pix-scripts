# Tests adaptatifs dans PIX

## Prérequis

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## Génération

- Télécharger les épreuves au format CSV depuis la vue JJV dans AirTable, les mettre dans `data`.
- `python epreuves.py` crée `epreuves.json` et `prerequis.json`
- `pypy dummy.py 20` crée un test adaptatif de profondeur au plus 20 (1 min environ) et un fichier `records.json` avec les scénarios
- `python json2csv.py` crée l'équivalent `records.csv`.

## Simulation

`python cat.py 20` permet de simuler le test adaptatif avec une interface en Flask.

## Mise en production

Dans une base `pg_staging` en local, importer les scénarios de la façon suivante :

    psql pg_staging
    # \copy scenarios("courseId",path,"nextChallengeId") from '/path/to/records.csv' delimiter ',' csv

Ensuite vous pourrez exporter seulement la table `scenarios` :

    pg_dump --data-only --table=scenarios pg_staging > scenarios.dump

Pour ensuite l'importer sur le serveur PIX :

    dokku postgres:connect pg-staging < scenarios.dump

(Attention, `pg-staging` est le nom de l'application Dokku, tandis que `pg_staging` est le nom de la base de données.)
