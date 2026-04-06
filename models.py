class Personnage:
    def __init__(self, nom, attaque, defense, pv):
        self.nom = nom
        self.attaque = attaque
        self.defense = defense
        self.pv_max = pv
        self.pv = pv

    def est_vivant(self):
        return self.pv > 0

    def recevoir_degats(self, degats_bruts):
        degats = max(0, degats_bruts - self.defense)
        self.pv = max(0, self.pv - degats)
        return degats

    def attaquer(self, cible):
        return cible.recevoir_degats(self.attaque)

    def __str__(self):
        return f"{self.nom} | ATK: {self.attaque} | DEF: {self.defense} | PV: {self.pv}/{self.pv_max}"

    @staticmethod
    def depuis_dict(data):
        return Personnage(
            nom=data["nom"],
            attaque=data["attaque"],
            defense=data["defense"],
            pv=data["pv"]
        )


class Monstre:
    def __init__(self, nom, attaque, defense, pv):
        self.nom = nom
        self.attaque = attaque
        self.defense = defense
        self.pv_max = pv
        self.pv = pv

    def est_vivant(self):
        return self.pv > 0

    def recevoir_degats(self, degats_bruts):
        degats = max(0, degats_bruts - self.defense)
        self.pv = max(0, self.pv - degats)
        return degats

    def attaquer(self, cible):
        return cible.recevoir_degats(self.attaque)

    def __str__(self):
        return f"{self.nom} | ATK: {self.attaque} | DEF: {self.defense} | PV: {self.pv}/{self.pv_max}"

    @staticmethod
    def depuis_dict(data):
        return Monstre(
            nom=data["nom"],
            attaque=data["attaque"],
            defense=data["defense"],
            pv=data["pv"]
        )


class Equipe:
    def __init__(self):
        self.personnages = []

    def ajouter(self, personnage):
        self.personnages.append(personnage)

    def est_en_vie(self):
        return any(p.est_vivant() for p in self.personnages)

    def membres_vivants(self):
        return [p for p in self.personnages if p.est_vivant()]

    def __str__(self):
        lignes = []
        for i, p in enumerate(self.personnages, 1):
            statut = "" if p.est_vivant() else " [MORT]"
            lignes.append(f"  {i}. {p}{statut}")
        return "\n".join(lignes)
