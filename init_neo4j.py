import os

from neo4j import GraphDatabase
import json
import re
import time

# Connexion à Neo4j
driver = GraphDatabase.driver("bolt://db_neo:7687", auth=("neo4j", "equipe23"))

for attempt in range(30):
    try:
        driver.verify_connectivity()
        break
    except:
        print(f"⏳ Waiting for Neo4j... ({attempt})")
        time.sleep(2)
else:
    raise RuntimeError("Neo4j did not become available in time.")

# Fonction pour nettoyer les ingrédients
def nettoyer_ingredient(texte):
    texte = re.sub(r"¼|½|¾","",texte)
    texte = re.sub(r"\d+\/\d+|\d+","",texte)
    texte = re.sub(r"\bc\.?\w*\s+à\s+(soupe|thé|café)\b","",texte)
    texte = re.sub(r"ml\s+|g\s+|kg\s+|oz\s+|boîte|paquet|tasse|œuf|gousse|environ|tbsp|pincées|litres", "",
                   texte, flags=re.IGNORECASE)
    texte = re.sub(r"bonnes|","",texte, flags=re.IGNORECASE)
    texte = re.sub(r"\(.*?\)", "", texte)
    texte = re.sub(r"\s*\d+", "", texte)
    texte = re.sub(r"^\s*(de\s+|d’|d'|ou\s+|du\s+)","",texte,flags=re.IGNORECASE)
    texte = re.sub(r"\s+", " ", texte)
    return texte.strip()

# Fonction d'import d'une recette
def importer_recette(tx, recette):
    # Nettoyage des champs
    nom_recette = recette.get("titre")
    if not nom_recette:
        print("⚠️ Recette ignorée : titre manquant")
        return  # on ignore cette recette

    auteur = recette.get("auteur")
    if not auteur:
        auteur = "Inconnu"

    types = recette.get("type_de_plat", [])
    description = recette.get("description")
    url = recette.get("url")
    portions = recette.get("portions")
    temps_cuisson = recette.get("temps_cuisson")
    if not temps_cuisson:
        temps_cuisson = "0"

    temps_preparation = recette.get("temps_preparation")
    if not temps_preparation:
        temps_preparation = "0"

    ingredients_bruts = recette.get("ingredients", [])
    ingredients = recette.get("ingredients", [])
    instructions = recette.get("instructions", [])

    # Créer la recette
    tx.run("""
         MERGE (r:Recette {name: $nom_recette})
         SET r.name = $nom_recette,
             r.description = $nom_recette,
             r.description2 = $description,
             r.temps_cuisson = $temps_cuisson,
             r.temps_preparation = $temps_preparation,
             r.portions = $portions,
             r.ingredients_bruts = $ingredients,
             r.instructions = $instructions,
             r.url = $url
         """, nom_recette=nom_recette, description=description, temps_cuisson=temps_cuisson,
           temps_preparation=temps_preparation, url=url, portions=portions,
           ingredients=ingredients, instructions=instructions)

    # Auteur
    tx.run("""
        MERGE (a:Auteur {nom: $auteur})
        MERGE (r:Recette {name: $nom_recette})
        MERGE (r)-[:ECRITE_PAR]->(a)
        """, auteur=auteur, nom_recette=nom_recette)

    # Type de plat
    for type_plat in types:
        tx.run("""
            MERGE (t:TypeDePlat {nom: $type})
            MERGE (r:Recette {name: $nom_recette})
            MERGE (r)-[:EST_DE_TYPE]->(t)
            """, type=type_plat, nom_recette=nom_recette)

    # Temps cuisson
    tx.run("""
        MERGE (tc:TempsCuisson {valeur: $temps})
        MERGE (r:Recette {name: $nom_recette})
        MERGE (r)-[:A_COMME_TEMPS_CUISSON]->(tc)
        """, temps=temps_cuisson, nom_recette=nom_recette)

    # Temps préparation
    tx.run("""
        MERGE (tp:TempsPreparation {valeur: $temps})
        MERGE (r:Recette {name: $nom_recette})
        MERGE (r)-[:A_COMME_TEMPS_PREPARATION]->(tp)
        """, temps=temps_preparation, nom_recette=nom_recette)

    # Ingrédients
    for brut in ingredients:
        nom_produit = nettoyer_ingredient(brut)
        tx.run("""
            MERGE (p:Produit {nom: $nom_produit})
            MERGE (r:Recette {name: $nom_recette})
            MERGE (r)-[:UTILISE]->(p)
            """, nom_produit=nom_produit, nom_recette=nom_recette)


# Charger et importer toutes les recettes depuis tous les fichiers JSON du dossier
dossier = "dump_recettes"

with driver.session() as session:
    for nom_fichier in os.listdir(dossier):
        if nom_fichier.endswith(".json"):
            chemin = os.path.join(dossier, nom_fichier)
            with open(chemin, encoding="utf-8") as f:
                data = json.load(f)
                for recette in data:
                    session.execute_write(importer_recette, recette)
