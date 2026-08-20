"""
Point d'entrée principal de l'application de Gestion des Employés et des Départements (Mode Console).
"""

import sys
from gestion_employes import GestionEmployes
from gestion_departements import GestionDepartements
from employe import Employe
from departement import Departement
from exceptions import (
    ApplicationError,
    SalaireInvalideError,
    AgeInvalideError,
    MatriculeInexistantError,
    DepartementIntrouvableError,
    FichierErreur
)
from utils import (
    saisir_chaine,
    saisir_entier,
    saisir_flottant,
    confirmer_action,
    afficher_titre
)


def recharger_donnees(gestion_emp: GestionEmployes, gestion_dept: GestionDepartements) -> None:
    """
    Recharge les données des départements et des employés au démarrage du programme.

    Args:
        gestion_emp (GestionEmployes): Gestionnaire des employés.
        gestion_dept (GestionDepartements): Gestionnaire des départements.
    """
    print("⏳ Chargement automatique des données...")
    try:
        gestion_dept.charger_depuis_json()
        gestion_emp.charger_depuis_json()
        print("✅ Données rechargées avec succès !")
    except FichierErreur as e:
        print(f"⚠️ Avertissement lors du chargement des données : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue lors de la lecture des fichiers : {e}")
    finally:
        print(f"📊 {len(gestion_dept.departements)} département(s) et {len(gestion_emp.employes)} employé(s) en mémoire.\n")


def sauvegarder_donnees(gestion_emp: GestionEmployes, gestion_dept: GestionDepartements, silencieux: bool = False) -> None:
    """
    Sauvegarde l'ensemble des données dans les fichiers JSON avec blocs try-except-finally.

    Args:
        gestion_emp (GestionEmployes): Gestionnaire des employés.
        gestion_dept (GestionDepartements): Gestionnaire des départements.
        silencieux (bool): Si True, réduit le niveau de détails affichés.
    """
    if not silencieux:
        print("⏳ Sauvegarde en cours des données...")
    try:
        gestion_dept.sauvegarder_dans_json()
        gestion_emp.sauvegarder_dans_json()
        if not silencieux:
            print("✅ Sauvegarde effectuée avec succès dans 'employes.json' et 'departements.json'.")
    except FichierErreur as e:
        print(f"❌ Erreur de sauvegarde : {e}")
    except Exception as e:
        print(f"❌ Erreur critique lors de la sauvegarde : {e}")
    finally:
        if not silencieux:
            print("--------------------------------------------------")


def menu_ajouter_employe(gestion_emp: GestionEmployes, gestion_dept: GestionDepartements) -> None:
    """
    Interface de saisie et d'ajout d'un nouvel employé.
    """
    afficher_titre("AJOUTER UN NOUVEL EMPLOYÉ")
    try:
        matricule = saisir_chaine("Matricule (ex: EMP005) : ").upper()

        if gestion_emp.employes.get(matricule):
            print(f"❌ Erreur : Le matricule '{matricule}' existe déjà.")
            return

        nom = saisir_chaine("Nom : ")
        prenom = saisir_chaine("Prénom : ")
        age = saisir_entier("Âge (entre 18 et 100) : ")
        sexe = saisir_chaine("Sexe (M/F/Autre) : ")
        adresse = saisir_chaine("Adresse : ")
        telephone = saisir_chaine("Téléphone : ")
        poste = saisir_chaine("Poste occupé : ")
        salaire = saisir_flottant("Salaire mensuel (€) : ", min_val=0.0)

        # Proposer d'affecter un département existant
        departement = "Non affecté"
        if gestion_dept.departements:
            print("\nDépartements disponibles : " + ", ".join(gestion_dept.departements.keys()))
            dept_code = input("Code du département (Laisser vide pour 'Non affecté') : ").strip().upper()
            if dept_code:
                if gestion_dept.existe(dept_code):
                    departement = dept_code
                else:
                    print(f"⚠️ Code '{dept_code}' introuvable. Affecté à 'Non affecté'.")

        emp = Employe(
            matricule=matricule,
            nom=nom,
            prenom=prenom,
            age=age,
            sexe=sexe,
            adresse=adresse,
            telephone=telephone,
            poste=poste,
            salaire=salaire,
            departement=departement
        )

        gestion_emp.ajouter_employe(emp)
        print(f"\n✅ L'employé {prenom} {nom} [{matricule}] a été ajouté avec succès !")

        # Sauvegarde automatique après ajout
        sauvegarder_donnees(gestion_emp, gestion_dept, silencieux=True)

    except (AgeInvalideError, SalaireInvalideError, ApplicationError) as e:
        print(f"❌ Impossible d'ajouter l'employé : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")


def menu_modifier_employe(gestion_emp: GestionEmployes, gestion_dept: GestionDepartements) -> None:
    """
    Interface de modification des informations d'un employé.
    """
    afficher_titre("MODIFIER UN EMPLOYÉ")
    try:
        matricule = saisir_chaine("Matricule de l'employé à modifier : ").upper()
        emp = gestion_emp.rechercher_employe(matricule)

        print("\nInformations actuelles :")
        emp.afficher()

        print("\nLaissez vide les champs que vous ne souhaitez pas modifier.")

        nom = input(f"Nouveau nom [{emp.nom}] : ").strip()
        prenom = input(f"Nouveau prénom [{emp.prenom}] : ").strip()

        age_input = input(f"Nouvel âge [{emp.age}] : ").strip()
        age = int(age_input) if age_input else None

        sexe = input(f"Nouveau sexe [{emp.sexe}] : ").strip()
        adresse = input(f"Nouvelle adresse [{emp.adresse}] : ").strip()
        telephone = input(f"Nouveau téléphone [{emp.telephone}] : ").strip()
        poste = input(f"Nouveau poste [{emp.poste}] : ").strip()

        salaire_input = input(f"Nouveau salaire [{emp.salaire} €] : ").strip()
        salaire = float(salaire_input) if salaire_input else None

        dept_code = input(f"Nouveau département [{emp.departement}] : ").strip().upper()
        if dept_code and not gestion_dept.existe(dept_code):
            raise DepartementIntrouvableError(dept_code)

        gestion_emp.modifier_employe(
            matricule=matricule,
            nom=nom,
            prenom=prenom,
            age=age,
            sexe=sexe,
            adresse=adresse,
            telephone=telephone,
            poste=poste,
            salaire=salaire,
            departement=dept_code if dept_code else None
        )

        print(f"\n✅ L'employé [{matricule}] a été mis à jour avec succès !")
        sauvegarder_donnees(gestion_emp, gestion_dept, silencieux=True)

    except (MatriculeInexistantError, DepartementIntrouvableError, AgeInvalideError, SalaireInvalideError) as e:
        print(f"❌ Modification échouée : {e}")
    except ValueError as e:
        print(f"❌ Valeur de saisie invalide : {e}")


def menu_supprimer_employe(gestion_emp: GestionEmployes, gestion_dept: GestionDepartements) -> None:
    """
    Interface de suppression d'un employé.
    """
    afficher_titre("SUPPRIMER UN EMPLOYÉ")
    try:
        matricule = saisir_chaine("Matricule de l'employé à supprimer : ").upper()
        emp = gestion_emp.rechercher_employe(matricule)

        print("\nFiche de l'employé à supprimer :")
        emp.afficher()

        if confirmer_action(f"Êtes-vous sûr de vouloir supprimer l'employé [{matricule}] ?"):
            gestion_emp.supprimer_employe(matricule)
            print(f"✅ Employé [{matricule}] supprimé définitivement.")
            sauvegarder_donnees(gestion_emp, gestion_dept, silencieux=True)
        else:
            print("Operation de suppression annulée.")

    except MatriculeInexistantError as e:
        print(f"❌ Suppression impossible : {e}")


def menu_rechercher_employe(gestion_emp: GestionEmployes) -> None:
    """
    Interface de recherche d'un employé par son matricule.
    """
    afficher_titre("RECHERCHER UN EMPLOYÉ")
    try:
        matricule = saisir_chaine("Entrez le matricule de l'employé : ").upper()
        emp = gestion_emp.rechercher_employe(matricule)
        print("\n--- EMPLOYÉ TROUVÉ ---")
        emp.afficher()
    except MatriculeInexistantError as e:
        print(f"❌ Recherche échouée : {e}")


def menu_statistiques(gestion_emp: GestionEmployes) -> None:
    """
    Affiche la vue statistique complète de l'entreprise.
    """
    afficher_titre("STATISTIQUES DE L'ENTREPRISE")
    stats = gestion_emp.calculer_statistiques()

    total = stats["total_employes"]
    print(f"📊 Nombre total d'employés    : {total}")
    print(f"💰 Salaire minimum            : {stats['salaire_min']:,.2f} €")
    print(f"💰 Salaire maximum            : {stats['salaire_max']:,.2f} €")
    print(f"📊 Salaire moyen              : {stats['salaire_moyen']:,.2f} €")
    print(f"💶 Masse salariale totale     : {stats['masse_salariale']:,.2f} €")

    print("\n--- Nombre d'employés par département ---")
    if not stats["par_departement"]:
        print("  Aucun département affecté.")
    else:
        for dept, nombre in stats["par_departement"].items():
            print(f"  • Département [{dept}] : {nombre} employé(s)")
    print("=" * 50)


def menu_gerer_departements(gestion_emp: GestionEmployes, gestion_dept: GestionDepartements) -> None:
    """
    Sous-menu interactif pour la gestion des départements.
    """
    while True:
        print("\n======================================")
        print("       GESTION DES DÉPARTEMENTS       ")
        print("======================================")
        print("1. Ajouter un département")
        print("2. Modifier un département")
        print("3. Supprimer un département")
        print("4. Afficher tous les départements")
        print("5. Affecter un employé à un département")
        print("6. Retour au menu principal")

        choix = input("Votre choix : ").strip()

        try:
            if choix == "1":
                afficher_titre("AJOUTER UN DÉPARTEMENT")
                code = saisir_chaine("Code du département (ex: IT, RH) : ").upper()
                nom = saisir_chaine("Nom du département : ")
                description = input("Description : ").strip()
                dept = Departement(code=code, nom=nom, description=description)
                gestion_dept.ajouter_departement(dept)
                print(f"✅ Département [{code}] ajouté avec succès !")
                sauvegarder_donnees(gestion_emp, gestion_dept, silencieux=True)

            elif choix == "2":
                afficher_titre("MODIFIER UN DÉPARTEMENT")
                code = saisir_chaine("Code du département à modifier : ").upper()
                dept = gestion_dept.rechercher_departement(code)
                print("Détails actuels :")
                dept.afficher()
                nouveau_nom = input(f"Nouveau nom [{dept.nom}] : ").strip()
                nouvelle_desc = input(f"Nouvelle description [{dept.description}] : ").strip()
                gestion_dept.modifier_departement(code, nouveau_nom or None, nouvelle_desc if nouvelle_desc else None)
                print(f"✅ Département [{code}] modifié avec succès !")
                sauvegarder_donnees(gestion_emp, gestion_dept, silencieux=True)

            elif choix == "3":
                afficher_titre("SUPPRIMER UN DÉPARTEMENT")
                code = saisir_chaine("Code du département à supprimer : ").upper()
                dept = gestion_dept.rechercher_departement(code)
                dept.afficher()
                if confirmer_action(f"Êtes-vous sûr de supprimer le département [{code}] ?"):
                    gestion_dept.supprimer_departement(code)
                    print(f"✅ Département [{code}] supprimé.")
                    sauvegarder_donnees(gestion_emp, gestion_dept, silencieux=True)

            elif choix == "4":
                gestion_dept.afficher_tous()

            elif choix == "5":
                afficher_titre("AFFECTER UN EMPLOYÉ À UN DÉPARTEMENT")
                matricule = saisir_chaine("Matricule de l'employé : ").upper()
                code_dept = saisir_chaine("Code du département cible : ").upper()
                emp = gestion_emp.affecter_departement(matricule, code_dept, gestion_dept)
                print(f"✅ L'employé [{emp.matricule}] a été affecté au département [{code_dept}] avec succès !")
                sauvegarder_donnees(gestion_emp, gestion_dept, silencieux=True)

            elif choix == "6":
                break
            else:
                print("❌ Choix invalide. Veuillez saisir un nombre entre 1 et 6.")

        except (DepartementIntrouvableError, MatriculeInexistantError, ValueError) as e:
            print(f"❌ Erreur : {e}")
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")


def main() -> None:
    """
    Fonction principale d'exécution de l'application terminal.
    """
    gestion_dept = GestionDepartements()
    gestion_emp = GestionEmployes()

    # Rechargement automatique des données au démarrage
    recharger_donnees(gestion_emp, gestion_dept)

    while True:
        print("\n======================================")
        print("         GESTION DES EMPLOYÉS         ")
        print("======================================")
        print("1. Ajouter un employé")
        print("2. Modifier un employé")
        print("3. Supprimer un employé")
        print("4. Rechercher un employé")
        print("5. Afficher tous les employés")
        print("6. Gérer les départements")
        print("7. Statistiques")
        print("8. Sauvegarder les données")
        print("9. Quitter")

        choix = input("Votre choix : ").strip()

        try:
            if choix == "1":
                menu_ajouter_employe(gestion_emp, gestion_dept)
            elif choix == "2":
                menu_modifier_employe(gestion_emp, gestion_dept)
            elif choix == "3":
                menu_supprimer_employe(gestion_emp, gestion_dept)
            elif choix == "4":
                menu_rechercher_employe(gestion_emp)
            elif choix == "5":
                gestion_emp.afficher_tous()
            elif choix == "6":
                menu_gerer_departements(gestion_emp, gestion_dept)
            elif choix == "7":
                menu_statistiques(gestion_emp)
            elif choix == "8":
                sauvegarder_donnees(gestion_emp, gestion_dept)
            elif choix == "9":
                sauvegarder_donnees(gestion_emp, gestion_dept, silencieux=True)
                print("\n👋 Merci d'avoir utilisé l'application de Gestion des Employés. Au revoir !")
                sys.exit(0)
            else:
                print("❌ Choix non reconnu. Veuillez choisir un numéro entre 1 et 9.")
        except KeyboardInterrupt:
            print("\n\n⚠️ Interruption détectée. Sauvegarde automatique des données...")
            sauvegarder_donnees(gestion_emp, gestion_dept, silencieux=True)
            print("👋 Au revoir !")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erreur non gérée dans le menu principal : {e}")


if __name__ == "__main__":
    main()
