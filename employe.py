"""
Module définissant la classe Employe qui hérite de Personne.
"""

from personne import Personne
from exceptions import SalaireInvalideError


class Employe(Personne):
    """
    Classe représentant un employé dans l'entreprise, héritant de Personne.

    Attributs privés supplémentaires:
        _matricule (str): Identifiant unique de l'employé.
        _poste (str): Intitulé du poste occupé.
        _salaire (float): Salaire mensuel de l'employé.
        _departement (str): Code ou nom du département auquel l'employé appartient.
    """

    def __init__(self, matricule: str, nom: str, prenom: str, age: int, sexe: str,
                 adresse: str, telephone: str, poste: str, salaire: float, departement: str = "Non affecté"):
        """
        Initialise un nouvel employé en appelant le constructeur de la classe parent Personne.

        Args:
            matricule (str): Identifiant unique (ex: EMP001).
            nom (str): Nom de l'employé.
            prenom (str): Prénom de l'employé.
            age (int): Âge de l'employé.
            sexe (str): Sexe de l'employé.
            adresse (str): Adresse de l'employé.
            telephone (str): Numéro de téléphone.
            poste (str): Intitulé du poste.
            salaire (float): Salaire de l'employé (doit être >= 0).
            departement (str): Code/Nom du département (par défaut 'Non affecté').

        Raises:
            SalaireInvalideError: Si le salaire est strictement négatif.
            AgeInvalideError: Si l'âge est invalide via Personne.
        """
        super().__init__(nom, prenom, age, sexe, adresse, telephone)
        self._matricule = matricule.strip().upper()
        self._poste = poste
        self.salaire = salaire  # Utilise le setter pour valider le salaire
        self._departement = departement

    @property
    def matricule(self) -> str:
        """Obtient le matricule de l'employé."""
        return self._matricule

    @matricule.setter
    def matricule(self, valeur: str):
        """Définit le matricule de l'employé."""
        if not valeur or not valeur.strip():
            raise ValueError("Le matricule ne peut pas être vide.")
        self._matricule = valeur.strip().upper()

    @property
    def poste(self) -> str:
        """Obtient le poste de l'employé."""
        return self._poste

    @poste.setter
    def poste(self, valeur: str):
        """Définit le poste de l'employé."""
        if not valeur or not valeur.strip():
            raise ValueError("Le poste ne peut pas être vide.")
        self._poste = valeur.strip()

    @property
    def salaire(self) -> float:
        """Obtient le salaire de l'employé."""
        return self._salaire

    @salaire.setter
    def salaire(self, valeur: float):
        """
        Définit le salaire de l'employé.

        Raises:
            SalaireInvalideError: Si le salaire est inférieur à 0.
        """
        try:
            valeur_flottante = float(valeur)
        except (ValueError, TypeError):
            raise SalaireInvalideError("Le salaire doit être un nombre valide.")

        if valeur_flottante < 0:
            raise SalaireInvalideError(f"Le salaire ({valeur_flottante} €) ne peut pas être négatif.")
        self._salaire = valeur_flottante

    @property
    def departement(self) -> str:
        """Obtient le département de l'employé."""
        return self._departement

    @departement.setter
    def departement(self, valeur: str):
        """Définit le département de l'employé."""
        self._departement = valeur.strip() if valeur else "Non affecté"

    def afficher(self) -> None:
        """
        Redéfinition polymorphique de la méthode afficher.
        Affiche l'ensemble des informations de l'employé, y compris son poste et son salaire.
        """
        print(f"--- Fiche Employé : [{self._matricule}] ---")
        super().afficher()
        print(f"Poste : {self._poste} | Département : {self._departement}")
        print(f"Salaire mensuel : {self._salaire:,.2f} €")
        print("-" * 40)

    def to_dict(self) -> dict:
        """
        Convertit l'objet Employe en dictionnaire JSON-compatible.

        Returns:
            dict: Données sérialisées de l'employé.
        """
        data = super().to_dict()
        data.update({
            "matricule": self._matricule,
            "poste": self._poste,
            "salaire": self._salaire,
            "departement": self._departement
        })
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crée une instance de Employe à partir d'un dictionnaire.

        Args:
            data (dict): Dictionnaire de données.

        Returns:
            Employe: Une nouvelle instance d'Employe.
        """
        return cls(
            matricule=data.get("matricule", ""),
            nom=data.get("nom", ""),
            prenom=data.get("prenom", ""),
            age=data.get("age", 18),
            sexe=data.get("sexe", "M"),
            adresse=data.get("adresse", ""),
            telephone=data.get("telephone", ""),
            poste=data.get("poste", ""),
            salaire=data.get("salaire", 0.0),
            departement=data.get("departement", "Non affecté")
        )
