"""
Module de vérification et de tests unitaires/d'intégration automatisés pour l'application.
"""

import os
import unittest
from personne import Personne
from employe import Employe
from departement import Departement
from gestion_employes import GestionEmployes
from gestion_departements import GestionDepartements
from exceptions import (
    SalaireInvalideError,
    AgeInvalideError,
    MatriculeInexistantError,
    DepartementIntrouvableError,
    FichierErreur
)


class TestGestionEmployesSystem(unittest.TestCase):
    """
    Suite de tests automatisés pour valider l'ensemble des contraintes techniques et fonctionnelles.
    """

    def setUp(self):
        """Initialise les objets de test avant chaque cas de test."""
        self.test_emp_file = "test_employes.json"
        self.test_dept_file = "test_departements.json"
        self.g_emp = GestionEmployes(self.test_emp_file)
        self.g_dept = GestionDepartements(self.test_dept_file)

    def tearDown(self):
        """Nettoie les fichiers temporaires créés durant les tests."""
        for filename in [self.test_emp_file, self.test_dept_file]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_01_heritage_et_encapsulation(self):
        """Vérifie l'héritage d'Employe à partir de Personne et l'encapsulation."""
        emp = Employe(
            matricule="TEST001",
            nom="Doe",
            prenom="John",
            age=30,
            sexe="M",
            adresse="123 Rue Test",
            telephone="0102030405",
            poste="Ingénieur",
            salaire=4000.0,
            departement="IT"
        )
        self.assertIsInstance(emp, Personne)
        self.assertIsInstance(emp, Employe)
        self.assertEqual(emp.matricule, "TEST001")
        self.assertEqual(emp.nom, "Doe")
        self.assertEqual(emp.salaire, 4000.0)

    def test_02_exceptions_validation(self):
        """Vérifie le déclenchement des exceptions personnalisées (SalaireInvalideError et AgeInvalideError)."""
        # Test âge invalide (<18)
        with self.assertRaises(AgeInvalideError):
            Personne(nom="Test", prenom="User", age=15, sexe="M", adresse="", telephone="")

        # Test salaire négatif (<0)
        with self.assertRaises(SalaireInvalideError):
            Employe(
                matricule="TEST002",
                nom="Test",
                prenom="User",
                age=25,
                sexe="F",
                adresse="",
                telephone="",
                poste="Dev",
                salaire=-500.0
            )

    def test_03_polymorphisme(self):
        """Vérifie l'existence et le comportement de la méthode afficher()."""
        p = Personne("NomP", "PrenomP", 25, "M", "Adr", "0123")
        e = Employe("T003", "NomE", "PrenomE", 30, "F", "Adr", "0123", "Chef", 3500.0, "IT")
        d = Departement("IT", "Informatique", "Desc")

        self.assertTrue(hasattr(p, "afficher"))
        self.assertTrue(hasattr(e, "afficher"))
        self.assertTrue(hasattr(d, "afficher"))

    def test_04_crud_et_exceptions_recherche(self):
        """Vérifie les opérations CRUD et les exceptions de recherche."""
        dept = Departement("DEV", "Développement", "Equipe dev")
        self.g_dept.ajouter_departement(dept)
        self.assertTrue(self.g_dept.existe("DEV"))

        emp = Employe("E01", "Alain", "Bernard", 40, "M", "Paris", "0600", "Lead", 5000.0, "DEV")
        self.g_emp.ajouter_employe(emp)

        # Recherche matricule existant
        self.assertEqual(self.g_emp.rechercher_employe("E01").nom, "Alain")

        # Recherche matricule inexistant -> MatriculeInexistantError
        with self.assertRaises(MatriculeInexistantError):
            self.g_emp.rechercher_employe("INEXISTANT")

        # Recherche département inexistant -> DepartementIntrouvableError
        with self.assertRaises(DepartementIntrouvableError):
            self.g_dept.rechercher_departement("INEXISTANT")

    def test_05_statistiques(self):
        """Vérifie la précision des calculs statistiques."""
        e1 = Employe("E1", "A", "B", 30, "M", "", "", "Dev", 2000.0, "IT")
        e2 = Employe("E2", "C", "D", 35, "F", "", "", "Dev", 4000.0, "IT")
        e3 = Employe("E3", "E", "F", 40, "M", "", "", "Manager", 6000.0, "RH")

        self.g_emp.ajouter_employe(e1)
        self.g_emp.ajouter_employe(e2)
        self.g_emp.ajouter_employe(e3)

        stats = self.g_emp.calculer_statistiques()
        self.assertEqual(stats["total_employes"], 3)
        self.assertEqual(stats["salaire_min"], 2000.0)
        self.assertEqual(stats["salaire_max"], 6000.0)
        self.assertEqual(stats["salaire_moyen"], 4000.0)
        self.assertEqual(stats["masse_salariale"], 12000.0)
        self.assertEqual(stats["par_departement"]["IT"], 2)
        self.assertEqual(stats["par_departement"]["RH"], 1)

    def test_06_persistance_json(self):
        """Vérifie la persistance et le rechargement JSON."""
        e = Employe("PERSIST1", "Json", "Test", 28, "M", "Nice", "0700", "Analyste", 3200.0, "FIN")
        self.g_emp.ajouter_employe(e)
        self.g_emp.sauvegarder_dans_json(self.test_emp_file)

        # Créer une nouvelle instance et recharger
        g_emp2 = GestionEmployes(self.test_emp_file)
        g_emp2.charger_depuis_json()
        self.assertIn("PERSIST1", g_emp2.employes)
        self.assertEqual(g_emp2.rechercher_employe("PERSIST1").nom, "Json")


if __name__ == "__main__":
    unittest.main()
