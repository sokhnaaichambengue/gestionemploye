"""
Module définissant la classe Departement.
"""


class Departement:
    """
    Classe représentant un département au sein de l'entreprise.

    Attributs privés:
        _code (str): Code unique identifiant le département (ex: 'IT', 'RH', 'FIN').
        _nom (str): Nom complet du département.
        _description (str): Description des activités du département.
    """

    def __init__(self, code: str, nom: str, description: str = ""):
        """
        Initialise un nouveau département.

        Args:
            code (str): Code du département.
            nom (str): Nom du département.
            description (str, optional): Description du département.
        """
        self._code = code.strip().upper()
        self._nom = nom.strip()
        self._description = description.strip()

    @property
    def code(self) -> str:
        """Obtient le code du département."""
        return self._code

    @code.setter
    def code(self, valeur: str):
        """Définit le code du département."""
        if not valeur or not valeur.strip():
            raise ValueError("Le code du département ne peut pas être vide.")
        self._code = valeur.strip().upper()

    @property
    def nom(self) -> str:
        """Obtient le nom du département."""
        return self._nom

    @nom.setter
    def nom(self, valeur: str):
        """Définit le nom du département."""
        if not valeur or not valeur.strip():
            raise ValueError("Le nom du département ne peut pas être vide.")
        self._nom = valeur.strip()

    @property
    def description(self) -> str:
        """Obtient la description du département."""
        return self._description

    @description.setter
    def description(self, valeur: str):
        """Définit la description du département."""
        self._description = valeur.strip() if valeur else ""

    def afficher(self) -> None:
        """
        Affiche les détails du département (Polymorphisme).
        """
        print(f"=== Département [{self._code}] ===")
        print(f"Nom : {self._nom}")
        print(f"Description : {self._description or 'Aucune description'}")
        print("=" * 40)

    def to_dict(self) -> dict:
        """
        Convertit le département en dictionnaire.

        Returns:
            dict: Représentation en dictionnaire.
        """
        return {
            "code": self._code,
            "nom": self._nom,
            "description": self._description
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crée une instance de Departement à partir d'un dictionnaire.

        Args:
            data (dict): Dictionnaire de données.

        Returns:
            Departement: Une nouvelle instance de Departement.
        """
        return cls(
            code=data.get("code", ""),
            nom=data.get("nom", ""),
            description=data.get("description", "")
        )
