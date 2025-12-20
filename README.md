# OPEN FOOD FACTS

## Acquisition des données
Assurez-vous d'avoir les fichiers `off.bson`, `off.metadata.json`, `fdc.bson` , `fdc.metadata.json` dans 
`mongo-init/dump_staging/` et le fichier `neo4j.dump` dans le dossier `neo4j_dumps` 
avant de démarrer le projet.

Vous pouvez les télécharger à partir du lien suivant: https://drive.google.com/drive/folders/1J_k_THGR2Lqr-zedXq59wOrOst0bbUg7?usp=sharing


Les fichiers `run_mongo_restore.sh` et `entrypoint.sh` doivent être en LF

## Configuration
L'application web est instanciée sur le port 80.

### Démarrage du projet
Pour partir le projet la première fois et lorsque que des dépendances sont ajoutées,
roulez la commande suivante:
```
docker compose up --build
```

Autrement, roulez cette commande-ci:
```
docker compose up
```

la restoration des dumps devraient ce faire automatiquement.

## Requêtes disponibles

### GET – Heartbeat (vérification du service)
Permet de vérifier que l’API est active et répond correctement.

#### Requête
```
GET /heartbeat
```

#### Réponse
200 - OK
```
{
  "nomApplication": "FoodFacts"
}
```

### GET – Données extraites (statistiques globales)
Retourne des statistiques agrégées calculées à partir :
- de la base de données MongoDB (Open Food Facts et FDC)
- de la base Neo4j (recettes de cuisine)

Ces données sont utilisées pour fournir une vue d’ensemble du contenu disponible dans l’application.

#### Requête
```
GET /extracted_data
```

#### Réponse
200 - OK
```
{
  "ndbProduitsAlimentairesScannes": int,
  "nbProduitsAlimentairesDeBases": int,
  "nbRecettesCuisine": int
}
```

### GET – Données transformées (statistiques globales)
Retourne des statistiques agrégées calculées à partir de notre bases de données MongoDB.
Ces données sont utilisées pour fournir une vue d’ensemble du contenu disponible dans l’application.

#### Requête
```
GET /transformed_data
```

#### Réponse
200 - OK
```
{
  "categoriesProduitAlimentaire": {
    "1120 - Fruits": int,
    "1210 - Légumes vert foncé": int,
    "1220 - Légumes jaune foncé ou orange": int,
    "1230 - Légumes féculents": int,
    "1240 - Autres légumes": int,
    "2100 - Grains entiers (100%)": int,
    "2210 - Aliments à grains entiers": int,

 [...]

 },
  "indicateursDeQualite": {
    "EcoScore": int,
    "Nova": int,
    "NutriScore": int
  }
}
```

### GET – ReadMe
Retourne la fichier README.md.

#### Requête
```
GET /readme
```

#### Réponse
200 - OK
```
# OPEN FOOD FACTS

## Acquisition des données
Assurez-vous d'avoir les fichiers `off.bson`, `off.metadata.json`, `fdc.bson` , `fdc.metadata.json` dans 
`mongo-init/dump_staging/` et le fichier `neo4j.dump` dans le dossier `neo4j_dumps` 
avant de démarrer le projet.

Vous pouvez les télécharger à partir du lien suivant: https://drive.google.com/drive/folders/1J_k_THGR2Lqr-zedXq59wOrOst0bbUg7?usp=sharing

## Configuration
L'application web est instanciée sur le port 80.

### Démarrage du projet
Pour partir le projet la première fois et lorsque que des dépendances sont ajoutées,
roulez la commande suivante:

[...]

```

### GET – Types de plats
Retourne la liste de tous les types de plats disponibles dans la base de données des recettes.
Les types de plats sont récupérés à partir des nœuds `TypeDePlat` stockés dans Neo4j.

#### Requête
```
GET /type
```

#### Réponse
200 - OK
```
[
  "30 minutes ou moins",
  "Pour enfants",
  "Sans cuisson",
  "Végétarien",
  "10 ingrédients ou moins",
  "Congelables",
  "Plat principal",
  "Dessert",
  "Plat d'accompagnement",
  "Boisson",
  "Soupe"
]
```

### POST – Recette selon type
Retourne une recette aléatoire qui répond aux types définis.

#### Paramètres
```
{
    "type": [
        str, 
        str,
        ...
    ]
}
```


#### Requête
```
POST /recette
```

#### Réponse
200 - OK
```
{
  "noPOST": "noRECETTE"
}
```

### POST – Recommandations de produits
Retourne pour chaque ingrédients d'une recette donnée une liste de recommandations de produits
selon les paramètres définis.

#### Paramètres
```
{
    "recette": {
        "nom": str,
        "ingredients": [
            ...
        ],
        "description": str,
        ...
    },
    "preferenceMarqueProduit": str,
    "indicateurDeQualiteSuperieurA": {
        "NutriScore": str,
        "Nova": str,
        "EcoScore": str
    },
}
```

#### Requête
```
POST /cuisiner
```

#### Réponse
200 - OK
```
...
```
