import random


class Membre:
    def __init__(self, nom: str, liste_ordonnee_choix: str):
        self.nom = nom
        self.liste = [int(choix) - 1 for choix in liste_ordonnee_choix.split('>')]

        self.sadness = 0
        self.current_choice = self.liste[0]

    def next_choice(self) -> int:
        self.sadness += 1
        self.current_choice = self.liste[self.sadness]
        return self.current_choice

    @property
    def is_last_choice(self):
        return self.sadness + 1 == len(self.liste)

    @property
    def score(self):
        if self.is_last_choice:
            return 99999
        else:
            next_project_fullness = len(current_matching.get_projet(self.liste[self.sadness + 1]).membres)
            if next_project_fullness > 5:
                return self.sadness + 10
            else:
                return self.sadness

    def __repr__(self):
        return "{} : projet n°{}".format(self.nom, self.current_choice + 1)


class Projet:
    def __init__(self, nom: str):
        self.membres = []
        self.nom = nom

    def add_member(self, member: Membre) -> Membre:
        self.membres.append(member)
        if len(self.membres) > 5:
            return self.__downgrade_one__()

    def __downgrade_one__(self) -> Membre:
        min_sadness = self.membres[0].sadness
        list_to_remove = []
        for membre in self.membres:
            if membre.sadness < min_sadness:
                list_to_remove = [membre]
            elif membre.sadness == min_sadness:
                list_to_remove.append(membre)

        if len(list_to_remove) == 1:
            to_remove = list_to_remove[0]
        else:
            to_remove = min(list_to_remove, key=lambda member: membre.score)

        self.membres.remove(to_remove)
        return to_remove

    def __repr__(self):
        return "{} :\n\t-".format(self.nom) + "\n\t-".join([str(membre) for membre in self.membres])


class Matching:
    def __init__(self):
        self.list_projets = [Projet("1. Il y a un ver au plafond !!! "),
                             Projet("2. Visualisation de données pour améliorer l'exploration de résultat génomiques"),
                             Projet("3. Modélisation de terrain 3D pour l'impression 3D et la navigation"),
                             Projet("4. Développement d'une application web de visualisation et de manipulation "
                                    "fragments de documents ancients"),
                             Projet("5. Pipeline de pré-traitement de jeu de données d’images IRM pour "
                                    "le deep learning"),
                             Projet("6. Neomics : nouvelle méthode pour l'intégration et la fouille "
                                    "de données (data mining) de données multi-omiques représentées dans une "
                                    "base de données orientée graphe (neo4j)"),
                             Projet("7. Mini Jeux Sérieux"),
                             Projet("8. Développement d’un modèle computationnel du sommeil paradoxal chez le rongeur")]

        self.list_membres = []

        with open("data.txt", 'r') as input_file:
            for line in input_file:
                line.strip()
                splitted_line = line.split()
                self.list_membres.append(Membre(" ".join(splitted_line[:-1]), splitted_line[-1]))

        random.shuffle(self.list_membres)
        for people in self.list_membres:
            self.add_membre(people)

        self.score_abs = sum([membre.sadness for membre in self.list_membres])
        max_sadness = sum([len(membre.liste) - 1 for membre in self.list_membres])
        self.score_rel = (max_sadness - self.score_abs) * 100 / max_sadness

    def add_membre(self, people: Membre):
        deleted_membre = self.list_projets[people.current_choice].add_member(people)
        if deleted_membre:
            deleted_membre.next_choice()
            self.add_membre(deleted_membre)

    def get_projet(self, project_number: int) -> Projet:
        return self.list_projets[project_number]

    def __repr__(self):
        return "SCORE = {} => {}% satisfaction".format(self.score_abs, self.score_rel)

    def print(self):
        print("\n".join(str(projet) for projet in self.list_projets) + "\n SCORE = {} => {}% satisfaction".format(
            self.score_abs, self.score_rel))


liste_matchings = []
for x in range(100):
    current_matching = Matching()
    liste_matchings.append(current_matching)

min(liste_matchings, key=lambda matching: matching.score_abs).print()
