"""
Module de gestion du CRUD des employés, du calcul des statistiques et de la persistance JSON.
"""

import json
import os
from typing import Dict, List, Optional
from employe import Employe
from gestion_departements import GestionDepartements
from exceptions import (
    MatriculeInexistantError,
    DepartementIntrouvableError,
    FichierErreur,
    SalaireInvalideError,
    AgeInvalideError
)


class GestionEmployes:
    """
    Classe gérans la collection des employés, les opérations CRUD, les statistiques et la persistance JSON.

    Attributs privés:
        _employes (Dict[str, Employe]): Dictionnaire des employés indexé par le matricule.
        _fichier_json (str): Chemin du fichier JSON de stockage.
    """

    def __init__(self, fichier_json: str = "employes.json"):
        """
        Initialise le gestionnaire d'employés.

        Args:
            fichier_json (str): Chemin du fichier JSON de persistance.
        """
        self._employes: Dict[str, Employe] = {}
        self._fichier_json = fichier_json

    @property
    def employes(self) -> Dict[str, Employe]:
        """Obtient le dictionnaire des employés."""
        return self._employes

    def ajouter_employe(self, employe: Employe) -> None:
        """
        Ajoute un nouvel employé dans le système.

        Args:
            employe (Employe): Instance de l'employé à ajouter.

        Raises:
            ValueError: Si un employé avec le même matricule existe déjà.
        """
        mat_cle = employe.matricule.upper()
        if mat_cle in self._employes:
            raise ValueError(f"Un employé avec le matricule '{mat_cle}' existe déjà.")
        self._employes[mat_cle] = employe

    def modifier_employe(self, matricule: str, **kwargs) -> Employe:
        """
        Modifie les informations d'un employé existant.

        Args:
            matricule (str): Matricule de l'employé à modifier.
            **kwargs: Clés/Valeurs des attributs à modifier (nom, prenom, age, sexe, adresse, telephone, poste, salaire, departement).

        Returns:
            Employe: L'instance de l'employé mis à jour.

        Raises:
            MatriculeInexistantError: Si le matricule n'existe pas.
            AgeInvalideError: Si l'âge fourni est invalide.
            SalaireInvalideError: Si le salaire fourni est invalide.
        """
        emp = self.rechercher_employe(matricule)

        if "nom" in kwargs and kwargs["nom"]:
            emp.nom = kwargs["nom"]
        if "prenom" in kwargs and kwargs["prenom"]:
            emp.prenom = kwargs["prenom"]
        if "age" in kwargs and kwargs["age"] is not None:
            emp.age = kwargs["age"]
        if "sexe" in kwargs and kwargs["sexe"]:
            emp.sexe = kwargs["sexe"]
        if "adresse" in kwargs and kwargs["adresse"]:
            emp.adresse = kwargs["adresse"]
        if "telephone" in kwargs and kwargs["telephone"]:
            emp.telephone = kwargs["telephone"]
        if "poste" in kwargs and kwargs["poste"]:
            emp.poste = kwargs["poste"]
        if "salaire" in kwargs and kwargs["salaire"] is not None:
            emp.salaire = kwargs["salaire"]
        if "departement" in kwargs and kwargs["departement"]:
            emp.departement = kwargs["departement"]

        return emp

    def supprimer_employe(self, matricule: str) -> Employe:
        """
        Supprime un employé du système.

        Args:
            matricule (str): Matricule de l'employé à supprimer.

        Returns:
            Employe: L'employé supprimé.

        Raises:
            MatriculeInexistantError: Si le matricule n'existe pas.
        """
        mat_cle = matricule.strip().upper()
        if mat_cle not in self._employes:
            raise MatriculeInexistantError(mat_cle)
        return self._employes.pop(mat_cle)

    def rechercher_employe(self, matricule: str) -> Employe:
        """
        Recherche un employé à partir de son matricule.

        Args:
            matricule (str): Matricule recherché.

        Returns:
            Employe: L'instance de l'employé trouvé.

        Raises:
            MatriculeInexistantError: Si aucun employé ne possède ce matricule.
        """
        mat_cle = matricule.strip().upper()
        if mat_cle not in self._employes:
            raise MatriculeInexistantError(mat_cle)
        return self._employes[mat_cle]

    def rechercher_par_nom(self, nom: str) -> List[Employe]:
        """
        Recherche les employés à partir de leur nom.

        Args:
            nom (str): Nom recherché.

        Returns:
            List[Employe]: Liste des employés correspondant au nom.
        """
        nom_recherche = nom.strip().lower()

        return [
            emp
            for emp in self._employes.values()
            if emp.nom.lower() == nom_recherche
        ]

    def affecter_departement(self, matricule: str, code_departement: str, gestion_dept: GestionDepartements) -> Employe:
        """
        Affecte un employé à un département.

        Args:
            matricule (str): Matricule de l'employé.
            code_departement (str): Code du département cible.
            gestion_dept (GestionDepartements): Instance du gestionnaire des départements pour vérification.

        Returns:
            Employe: L'employé avec le département mis à jour.

        Raises:
            MatriculeInexistantError: Si le matricule n'existe pas.
            DepartementIntrouvableError: Si le département n'existe pas.
        """
        emp = self.rechercher_employe(matricule)
        dept = gestion_dept.rechercher_departement(code_departement)
        emp.departement = dept.code
        return emp

    def obtenir_tous(self) -> List[Employe]:
        """
        Retourne la liste de tous les employés.

        Returns:
            List[Employe]: Liste des employés.
        """
        return list(self._employes.values())

    def afficher_tous(self) -> None:
        """
        Affiche la liste complète des employés enregistrés (Polymorphisme).
        """
        if not self._employes:
            print("Aucun employé n'est enregistré dans le système.")
            return

        print(f"\n================ LISTE DES EMPLOYÉS ({len(self._employes)}) ================")
        for emp in self._employes.values():
            emp.afficher()

    def calculer_statistiques(self) -> dict:
        """
        Calcule les statistiques clés de la masse salariale et de la répartition des employés.

        Returns:
            dict: Dictionnaire contenant:
                - total_employes (int)
                - salaire_min (float)
                - salaire_max (float)
                - salaire_moyen (float)
                - masse_salariale (float)
                - par_departement (dict)
        """
        if not self._employes:
            return {
                "total_employes": 0,
                "salaire_min": 0.0,
                "salaire_max": 0.0,
                "salaire_moyen": 0.0,
                "masse_salariale": 0.0,
                "par_departement": {}
            }

        salaires = [emp.salaire for emp in self._employes.values()]
        masse_salariale = sum(salaires)
        total = len(self._employes)
        salaire_min = min(salaires)
        salaire_max = max(salaires)
        salaire_moyen = masse_salariale / total if total > 0 else 0.0

        par_dept: Dict[str, int] = {}
        for emp in self._employes.values():
            dept_code = emp.departement
            par_dept[dept_code] = par_dept.get(dept_code, 0) + 1

        return {
            "total_employes": total,
            "salaire_min": salaire_min,
            "salaire_max": salaire_max,
            "salaire_moyen": salaire_moyen,
            "masse_salariale": masse_salariale,
            "par_departement": par_dept
        }

    def sauvegarder_dans_json(self, fichier_chemin: Optional[str] = None) -> None:
        """
        Sauvegarde tous les employés dans un fichier JSON avec gestion des exceptions try-except-finally.

        Args:
            fichier_chemin (str, optional): Chemin du fichier JSON cible.

        Raises:
            FichierErreur: En cas d'échec d'écriture dans le fichier JSON.
        """
        cible = fichier_chemin or self._fichier_json
        fichier_handle = None
        try:
            donnees = [emp.to_dict() for emp in self._employes.values()]
            fichier_handle = open(cible, "w", encoding="utf-8")
            json.dump(donnees, fichier_handle, indent=4, ensure_ascii=False)
        except Exception as err:
            raise FichierErreur(f"Impossible d'écrire dans le fichier '{cible}': {str(err)}")
        finally:
            if fichier_handle:
                fichier_handle.close()

    def charger_depuis_json(self, fichier_chemin: Optional[str] = None) -> None:
        """
        Recharge automatiquement les employés depuis le fichier JSON.

        Args:
            fichier_chemin (str, optional): Chemin du fichier JSON source.

        Raises:
            FichierErreur: En cas d'erreur de lecture du fichier JSON.
        """
        cible = fichier_chemin or self._fichier_json
        if not os.path.exists(cible):
            self._employes = {}
            return

        fichier_handle = None
        try:
            fichier_handle = open(cible, "r", encoding="utf-8")
            donnees = json.load(fichier_handle)
            self._employes = {}
            for item in donnees:
                emp = Employe.from_dict(item)
                self._employes[emp.matricule] = emp
        except json.JSONDecodeError as err:
            raise FichierErreur(f"Le fichier '{cible}' contient un JSON invalide : {str(err)}")
        except Exception as err:
            raise FichierErreur(f"Impossible de lire le fichier '{cible}': {str(err)}")
        finally:
            if fichier_handle:
                fichier_handle.close()
