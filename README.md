# ⚔️ Jeu de Combat par Vagues

Jeu en ligne de commande Python utilisant MongoDB pour stocker personnages, monstres et scores.

## Prérequis

- Python >= 3.8
- MongoDB en cours d'exécution sur `localhost:27017`
- Bibliothèque pymongo :

```bash
pip install pymongo
```

## Structure du projet

```
jeu_video_python/
├── main.py       # Menu principal et point d'entrée
├── db_init.py    # Initialisation de la base MongoDB
├── game.py       # Logique de combat et création d'équipe
├── models.py     # Classes Personnage, Monstre, Equipe
├── utils.py      # Connexion DB, affichage, classement
└── README.md
```

## Lancement

### 1. Initialiser la base de données (une seule fois)

```bash
python db_init.py
```

### 2. Lancer le jeu

```bash
python main.py
```

## Règles du jeu

- Compose une équipe de **3 personnages** parmi 10 disponibles.
- Affronte des **monstres aléatoires** vague après vague.
- Chaque personnage attaque d'abord, puis le monstre attaque un membre aléatoire.
- La **défense** réduit les dégâts reçus (dégâts = ATK adverse − DEF propre, minimum 0).
- Le jeu se termine quand tous tes personnages sont à 0 PV.
- Ton score (vagues survécues) est sauvegardé dans le **top 3**.

## Personnages disponibles

| Nom        | ATK | DEF | PV  |
|------------|-----|-----|-----|
| Guerrier   | 15  | 10  | 100 |
| Mage       | 20  |  5  |  80 |
| Archer     | 18  |  7  |  90 |
| Voleur     | 22  |  8  |  85 |
| Paladin    | 14  | 12  | 110 |
| Sorcier    | 25  |  3  |  70 |
| Chevalier  | 17  | 15  | 120 |
| Moine      | 19  |  9  |  95 |
| Berserker  | 23  |  6  | 105 |
| Chasseur   | 16  | 11  | 100 |
