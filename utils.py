"""
utils.py
Fonctions utilitaires : connexion DB, affichage, classement.
"""

from pymongo import MongoClient, DESCENDING

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "jeu_video"

# ── Connexion ────────────────────────────────────────────────────────────────

def get_db():
    """Retourne l'objet base de données MongoDB."""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]


# ── Récupération des données ─────────────────────────────────────────────────

def get_tous_personnages():
    """Retourne la liste de tous les documents personnages."""
    db = get_db()
    return list(db.personnages.find({}, {"_id": 0}))


def get_monstre_aleatoire():
    """Retourne un document monstre tiré aléatoirement."""
    db = get_db()
    pipeline = [{"$sample": {"size": 1}}]
    resultats = list(db.monstres.aggregate(pipeline))
    if not resultats:
        raise RuntimeError("Aucun monstre trouvé en base. Lance d'abord db_init.py.")
    doc = resultats[0]
    doc.pop("_id", None)
    return doc


# ── Classement ───────────────────────────────────────────────────────────────

def sauvegarder_score(nom_joueur, vagues):
    """Enregistre le score si il fait partie du top 3."""
    db = get_db()
    db.scores.insert_one({"joueur": nom_joueur, "vagues": vagues})
    # On ne conserve que les 3 meilleurs
    tous = list(db.scores.find().sort("vagues", DESCENDING))
    if len(tous) > 3:
        ids_a_supprimer = [doc["_id"] for doc in tous[3:]]
        db.scores.delete_many({"_id": {"$in": ids_a_supprimer}})


def get_classement():
    """Retourne les 3 meilleurs scores triés."""
    db = get_db()
    return list(db.scores.find({}, {"_id": 0}).sort("vagues", DESCENDING).limit(3))


# ── Affichage ────────────────────────────────────────────────────────────────

SEPARATEUR = "═" * 50

def afficher_titre():
    print("\n" + SEPARATEUR)
    print("          ⚔️   JEU DE COMBAT PAR VAGUES   ⚔️")
    print(SEPARATEUR)


def afficher_classement():
    classement = get_classement()
    print("\n" + SEPARATEUR)
    print("            🏆  MEILLEURS SCORES  🏆")
    print(SEPARATEUR)
    if not classement:
        print("  Aucun score enregistré pour le moment.")
    else:
        medailles = ["🥇", "🥈", "🥉"]
        for i, entry in enumerate(classement):
            medaille = medailles[i] if i < 3 else "  "
            print(f"  {medaille}  {entry['joueur']:<20} {entry['vagues']} vague(s)")
    print(SEPARATEUR + "\n")


def afficher_liste_personnages(personnages):
    print("\n" + "─" * 50)
    print("  PERSONNAGES DISPONIBLES")
    print("─" * 50)
    for i, p in enumerate(personnages, 1):
        print(f"  {i:>2}. {p['nom']:<12} ATK: {p['attaque']:>2}  DEF: {p['defense']:>2}  PV: {p['pv']:>3}")
    print("─" * 50)


def afficher_equipe(equipe):
    print("\n  📋 Équipe actuelle :")
    if not equipe.personnages:
        print("     (vide)")
    else:
        print(str(equipe))


def saisir_entier(message, min_val, max_val):
    """Demande un entier à l'utilisateur dans un intervalle donné."""
    while True:
        try:
            valeur = int(input(message))
            if min_val <= valeur <= max_val:
                return valeur
            print(f"  ⚠️  Entrez un nombre entre {min_val} et {max_val}.")
        except ValueError:
            print("  ⚠️  Entrée invalide. Veuillez entrer un nombre entier.")


def saisir_nom():
    """Demande un nom non vide à l'utilisateur."""
    while True:
        nom = input("  Votre nom d'utilisateur : ").strip()
        if nom:
            return nom
        print("  ⚠️  Le nom ne peut pas être vide.")
