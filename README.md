# OPEN FOOD FACTS
## Configuration
Pour partir le projet la première fois et lorsque que ajoute des dépendances:
`docker compose up --build`

Ensuite seulement:
`docker compose up`

### Bases de données
##### MongoDB
Pour tester mongo db:

ne pas oublier d'extraire off.tar.gz et fdc.tar.gz dans dump_staging 

```
docker exec -it db_mongo bash
mongosh --host localhost --port 27017
```

#### Neo4j
Pour tester neo4j db:

```
docker exec -it db_neo4j bash
cypher-shell
```

entrer le username
entrer le password

ou

Aller sur http://localhost:7474/ et connectez-vous.

#### to restore MongoDB

```
docker cp ["Chemin dossier local pulled"] db_mongo:/data/dump_staging
docker exec -it db_mongo bash
```
dans le root de mongodb
```
mongorestore  --db=db_mongo /data/dump_staging/
```

#### to create Dump
dans le root de mongodb
```
mongodump --db=db_mongo --collection=["la collection a dump"] --out /data/["nom de votre dossier dump"]
```
dans le docker container
```
docker cp db_mongo:/data/["nom de votre dossier dump"] ["Chemin dossier local sauvegarde"]
```