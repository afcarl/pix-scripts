# Tests adaptatifs dans PIX

## Prérequis

- Python 3 ou PyPy 3
- Graphviz si vous souhaitez afficher un test adaptatif

## Génération

- Télécharger les épreuves au format CSV depuis la vue JJV dans AirTable, les mettre dans `data`.
- `python3 epreuves.py` crée `epreuves.json` et `prerequis.json`.
- `pypy3 dummy.py 20 {{ test_id }}` crée un test adaptatif d'ID `{{ test_id }}` de profondeur au plus 20 et l'enregistre au format JSON (`scenarios.json`, 2 min de cuisson environ sur un MBA i5 1.3 GHz mid-2013).
- `python3 json2csv.py` crée l'équivalent `scenarios.csv`.
- `python3 airtable.py {{ test_id }}` permet de mettre à jour le test dans Airtable avec les bonnes épreuves.

## Simulation

`python3 cat.py 20` permet de simuler le test adaptatif avec une interface en Flask.

## Mise en production

Dans une base `pg_staging` en local, importer les scénarios de la façon suivante :

    psql pg_staging
    # \copy scenarios("courseId",path,"nextChallengeId") from '/path/to/scenarios.csv' delimiter ',' csv

Ensuite vous pourrez exporter seulement la table `scenarios` :

    pg_dump --data-only --table=scenarios pg_staging > scenarios.dump

Pour ensuite l'importer sur le serveur PIX :

    dokku postgres:connect pg-staging < scenarios.dump

(Attention, `pg-staging` (avec un dash) est le nom de l'application Dokku, tandis que `pg_staging` (avec un underscore) est le nom de la base de données.)
