"""
Module de gestion du CRUD et de la persistance des départements.
"""

import json
import os
from typing import Dict, List, Optional
from departement import Departement
from exceptions import DepartementIntrouvableError, FichierErreur


class GestionDepartements:
    """
    Classe gérant la liste des départements, les opérations CRUD et la persistance JSON.

    Attributs privés:
        _departements (Dict[str, Departement]): Dictionnaire indexé par le code du département.
        _fichier_json (str): Chemin du fichier de stockage JSON.
    """

    def __init__(self, fichier_json: str = "departements.json"):
        """
        Initialise le gestionnaire de départements.

        Args:
            fichier_json (str): Chemin vers le fichier de persistance JSON.
        """
        self._departements: Dict[str, Departement] = {}
        self._fichier_json = fichier_json

    @property
    def departements(self) -> Dict[str, Departement]:
        """Obtient le dictionnaire des départements."""
        return self._departements

    def ajouter_departement(self, departement: Departement) -> None:
        """
        Ajoute un nouveau département.

        Args:
            departement (Departement): Instance du département à ajouter.

        Raises:
            ValueError: Si un département avec le même code existe déjà.
        """
        code_cle = departement.code.upper()
        if code_cle in self._departements:
            raise ValueError(f"Un département avec le code '{code_cle}' existe déjà.")
        self._departements[code_cle] = departement

    def modifier_departement(self, code: str, nouveau_nom: Optional[str] = None, nouvelle_description: Optional[str] = None) -> Departement:
        """
        Modifie les informations d'un département existant.

        Args:
            code (str): Code du département à modifier.
            nouveau_nom (str, optional): Nouveau nom du département.
            nouvelle_description (str, optional): Nouvelle description.

        Returns:
            Departement: Le département mis à jour.

        Raises:
            DepartementIntrouvableError: Si le code n'existe pas.
        """
        dept = self.rechercher_departement(code)
        if nouveau_nom and nouveau_nom.strip():
            dept.nom = nouveau_nom
        if nouvelle_description is not None:
            dept.description = nouvelle_description
        return dept

    def supprimer_departement(self, code: str) -> Departement:
        """
        Supprime un département du système.

        Args:
            code (str): Code du département à supprimer.

        Returns:
            Departement: Le département supprimé.

        Raises:
            DepartementIntrouvableError: Si le code n'existe pas.
        """
        code_cle = code.strip().upper()
        if code_cle not in self._departements:
            raise DepartementIntrouvableError(code_cle)
        return self._departements.pop(code_cle)

    def rechercher_departement(self, code: str) -> Departement:
        """
        Recherche un département à partir de son code.

        Args:
            code (str): Code du département.

        Returns:
            Departement: L'instance du département trouvé.

        Raises:
            DepartementIntrouvableError: Si le département est introuvable.
        """
        code_cle = code.strip().upper()
        if code_cle not in self._departements:
            raise DepartementIntrouvableError(code_cle)
        return self._departements[code_cle]

    def existe(self, code: str) -> bool:
        """
        Vérifie si un département existe par son code.

        Args:
            code (str): Code du département.

        Returns:
            bool: True si le département existe, False sinon.
        """
        return code.strip().upper() in self._departements

    def obtenir_tous(self) -> List[Departement]:
        """
        Obtient la liste de tous les départements.

        Returns:
            List[Departement]: Liste des départements enregistrés.
        """
        return list(self._departements.values())

    def afficher_tous(self) -> None:
        """
        Affiche l'ensemble des départements enregistrés.
        """
        if not self._departements:
            print("Aucun département n'est enregistré dans le système.")
            return

        print(f"\n================ LISTE DES DÉPARTEMENTS ({len(self._departements)}) ================")
        for dept in self._departements.values():
            dept.afficher()

    def sauvegarder_dans_json(self, fichier_chemin: Optional[str] = None) -> None:
        """
        Sauvegarde tous les départements dans un fichier JSON avec gestion des exceptions.

        Args:
            fichier_chemin (str, optional): Chemin du fichier JSON cible.

        Raises:
            FichierErreur: En cas d'erreur d'écriture dans le fichier.
        """
        cible = fichier_chemin or self._fichier_json
        fichier_handle = None
        try:
            donnees = [dept.to_dict() for dept in self._departements.values()]
            fichier_handle = open(cible, "w", encoding="utf-8")
            json.dump(donnees, fichier_handle, indent=4, ensure_ascii=False)
        except Exception as err:
            raise FichierErreur(f"Impossible d'écrire dans le fichier '{cible}': {str(err)}")
        finally:
            if fichier_handle:
                fichier_handle.close()

    def charger_depuis_json(self, fichier_chemin: Optional[str] = None) -> None:
        """
        Recharge automatiquement les départements depuis le fichier JSON.

        Args:
            fichier_chemin (str, optional): Chemin du fichier JSON source.

        Raises:
            FichierErreur: En cas d'erreur de lecture du fichier.
        """
        cible = fichier_chemin or self._fichier_json
        if not os.path.exists(cible):
            # Si le fichier n'existe pas, on initialise avec un fichier vide
            self._departements = {}
            return

        fichier_handle = None
        try:
            fichier_handle = open(cible, "r", encoding="utf-8")
            donnees = json.load(fichier_handle)
            self._departements = {}
            for item in donnees:
                dept = Departement.from_dict(item)
                self._departements[dept.code] = dept
        except json.JSONDecodeError as err:
            raise FichierErreur(f"Le fichier '{cible}' contient un JSON invalide : {str(err)}")
        except Exception as err:
            raise FichierErreur(f"Impossible de lire le fichier '{cible}': {str(err)}")
        finally:
            if fichier_handle:
                fichier_handle.close()
