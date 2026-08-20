"""
Module définissant la classe Personne avec encapsulation et gestion de l'âge.
"""

from exceptions import AgeInvalideError


class Personne:
    """
    Classe représentant une personne physique.

    Attributs privés:
        _nom (str): Le nom de la personne.
        _prenom (str): Le prénom de la personne.
        _age (int): L'âge de la personne.
        _sexe (str): Le sexe de la personne (ex: 'M', 'F', 'Autre').
        _adresse (str): L'adresse de résidence.
        _telephone (str): Le numéro de téléphone.
    """

    def __init__(self, nom: str, prenom: str, age: int, sexe: str, adresse: str, telephone: str):
        """
        Initialise une nouvelle instance de la classe Personne.

        Args:
            nom (str): Nom de la personne.
            prenom (str): Prénom de la personne.
            age (int): Âge de la personne (doit être >= 18).
            sexe (str): Sexe de la personne.
            adresse (str): Adresse complète.
            telephone (str): Numéro de téléphone.

        Raises:
            AgeInvalideError: Si l'âge spécifié est inférieur à 18 ou supérieur à 100.
        """
        self._nom = nom
        self._prenom = prenom
        self.age = age  # Utilise le setter pour valider l'âge
        self._sexe = sexe
        self._adresse = adresse
        self._telephone = telephone

    @property
    def nom(self) -> str:
        """Obtient le nom de la personne."""
        return self._nom

    @nom.setter
    def nom(self, valeur: str):
        """Définit le nom de la personne."""
        if not valeur or not valeur.strip():
            raise ValueError("Le nom ne peut pas être vide.")
        self._nom = valeur.strip()

    @property
    def prenom(self) -> str:
        """Obtient le prénom de la personne."""
        return self._prenom

    @prenom.setter
    def prenom(self, valeur: str):
        """Définit le prénom de la personne."""
        if not valeur or not valeur.strip():
            raise ValueError("Le prénom ne peut pas être vide.")
        self._prenom = valeur.strip()

    @property
    def age(self) -> int:
        """Obtient l'âge de la personne."""
        return self._age

    @age.setter
    def age(self, valeur: int):
        """
        Définit l'âge de la personne.

        Raises:
            AgeInvalideError: Si l'âge n'est pas un entier valide entre 18 et 100.
        """
        try:
            valeur_int = int(valeur)
        except (ValueError, TypeError):
            raise AgeInvalideError("L'âge doit être un nombre entier valide.")

        if valeur_int < 18 or valeur_int > 100:
            raise AgeInvalideError(f"L'âge ({valeur_int}) est invalide. Il doit être compris entre 18 et 100 ans.")
        self._age = valeur_int

    @property
    def sexe(self) -> str:
        """Obtient le sexe de la personne."""
        return self._sexe

    @sexe.setter
    def sexe(self, valeur: str):
        """Définit le sexe de la personne."""
        self._sexe = valeur.strip() if valeur else "Non spécifié"

    @property
    def adresse(self) -> str:
        """Obtient l'adresse de la personne."""
        return self._adresse

    @adresse.setter
    def adresse(self, valeur: str):
        """Définit l'adresse de la personne."""
        self._adresse = valeur.strip() if valeur else "Non renseignée"

    @property
    def telephone(self) -> str:
        """Obtient le numéro de téléphone de la personne."""
        return self._telephone

    @telephone.setter
    def telephone(self, valeur: str):
        """Définit le numéro de téléphone de la personne."""
        self._telephone = valeur.strip() if valeur else "Non renseigné"

    def afficher(self) -> None:
        """
        Affiche les informations générales de la personne.
        Méthode conçue pour être redéfinie dans les classes dérivées (Polymorphisme).
        """
        print(f"Nom complet : {self._prenom} {self._nom}")
        print(f"Âge : {self._age} ans | Sexe : {self._sexe}")
        print(f"Adresse : {self._adresse} | Tél : {self._telephone}")

    def to_dict(self) -> dict:
        """
        Convertit l'objet Personne en dictionnaire.

        Returns:
            dict: Représentation sous forme de dictionnaire.
        """
        return {
            "nom": self._nom,
            "prenom": self._prenom,
            "age": self._age,
            "sexe": self._sexe,
            "adresse": self._adresse,
            "telephone": self._telephone
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crée une instance de Personne à partir d'un dictionnaire.

        Args:
            data (dict): Dictionnaire contenant les données.

        Returns:
            Personne: Une nouvelle instance de Personne.
        """
        return cls(
            nom=data.get("nom", ""),
            prenom=data.get("prenom", ""),
            age=data.get("age", 18),
            sexe=data.get("sexe", "M"),
            adresse=data.get("adresse", ""),
            telephone=data.get("telephone", "")
        )
