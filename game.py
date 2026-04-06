"""
game.py
Gestion de la création d'équipe et de la boucle de combat.
"""

import random
from models import Personnage, Monstre, Equipe
from utils import (
    get_tous_personnages,
    get_monstre_aleatoire,
    sauvegarder_score,
    afficher_liste_personnages,
    afficher_equipe,
    saisir_entier,
    SEPARATEUR,
)

TAILLE_EQUIPE = 3


# ── Création d'équipe ────────────────────────────────────────────────────────

def creer_equipe():
    """Interactif : le joueur compose son équipe de 3 personnages."""
    tous = get_tous_personnages()
    if len(tous) < TAILLE_EQUIPE:
        raise RuntimeError("Pas assez de personnages en base. Lance db_init.py.")

    equipe = Equipe()
    indices_choisis = set()

    print(f"\n  Compose ton équipe ({TAILLE_EQUIPE} personnages).")

    while len(equipe.personnages) < TAILLE_EQUIPE:
        afficher_liste_personnages(tous)
        afficher_equipe(equipe)

        # Filtre les personnages encore disponibles
        disponibles = [i for i in range(len(tous)) if i not in indices_choisis]
        print(f"\n  Slot {len(equipe.personnages) + 1}/{TAILLE_EQUIPE} — choisis un personnage (1-{len(tous)}) :")

        choix = saisir_entier("  > ", 1, len(tous)) - 1  # indice 0-based

        if choix in indices_choisis:
            print("  ⚠️  Ce personnage est déjà dans ton équipe. Choisis-en un autre.")
            continue

        indices_choisis.add(choix)
        p = Personnage.depuis_dict(tous[choix])
        equipe.ajouter(p)
        print(f"  ✅  {p.nom} ajouté à l'équipe !")

    print("\n" + SEPARATEUR)
    print("  ⚔️  Équipe finale :")
    print(str(equipe))
    print(SEPARATEUR)
    return equipe


# ── Combat ───────────────────────────────────────────────────────────────────

def _afficher_etat_combat(equipe, monstre, vague):
    print(f"\n{'─' * 50}")
    print(f"  🌊 VAGUE {vague}")
    print(f"{'─' * 50}")
    print(f"  👹 Monstre : {monstre}")
    print(f"{'─' * 50}")
    print("  🗡️  Ton équipe :")
    print(str(equipe))
    print(f"{'─' * 50}")


def combattre_vague(equipe, monstre, vague):
    """
    Résout un combat entre l'équipe et le monstre.
    Retourne True si l'équipe gagne, False sinon.
    """
    _afficher_etat_combat(equipe, monstre, vague)
    input("\n  [Appuie sur Entrée pour commencer le combat...]")

    while monstre.est_vivant() and equipe.est_en_vie():

        # ── Phase attaque de l'équipe ────────────────────────────────────────
        print(f"\n  ⚔️  L'équipe attaque {monstre.nom} !")
        for perso in equipe.membres_vivants():
            degats = perso.attaquer(monstre)
            print(f"     {perso.nom} inflige {degats} dégâts → {monstre.nom} PV : {max(0, monstre.pv)}")
            if not monstre.est_vivant():
                break  # Le monstre est mort, inutile de continuer

        if not monstre.est_vivant():
            break

        # ── Phase attaque du monstre ─────────────────────────────────────────
        cible = random.choice(equipe.membres_vivants())
        degats = monstre.attaquer(cible)
        print(f"\n  💥  {monstre.nom} attaque {cible.nom} → {degats} dégâts"
              f"  ({cible.nom} PV restants : {cible.pv})")

        if not cible.est_vivant():
            print(f"  💀  {cible.nom} est hors combat !")

    # ── Résultat ─────────────────────────────────────────────────────────────
    if not monstre.est_vivant():
        print(f"\n  🎉 Victoire ! {monstre.nom} est vaincu !")
        return True
    else:
        print("\n  💀 Défaite... Toute l'équipe a été vaincue.")
        return False


# ── Boucle principale de jeu ─────────────────────────────────────────────────

def lancer_partie(nom_joueur):
    """Lance une partie complète pour un joueur."""
    print(f"\n  Bienvenue, {nom_joueur} ! Compose ton équipe.")
    equipe = creer_equipe()

    vague = 0
    print("\n  🚀 Le combat commence !")

    while True:
        vague += 1
        # Crée un nouvel objet monstre frais depuis la DB
        data_monstre = get_monstre_aleatoire()
        monstre = Monstre.depuis_dict(data_monstre)

        victoire = combattre_vague(equipe, monstre, vague)

        if not victoire:
            break  # Défaite

        # Petite pause entre les vagues
        print(f"\n  🌟 Tu as survécu à la vague {vague} !")
        input("  [Appuie sur Entrée pour la prochaine vague...]")

    # ── Fin de partie ────────────────────────────────────────────────────────
    vagues_survecues = vague - 1  # La dernière vague = défaite
    print(f"\n{SEPARATEUR}")
    print(f"  🏁 Partie terminée, {nom_joueur} !")
    print(f"     Vagues survécues : {vagues_survecues}")
    print(SEPARATEUR)

    sauvegarder_score(nom_joueur, vagues_survecues)
    print("  ✅  Score sauvegardé.")

    return vagues_survecues
