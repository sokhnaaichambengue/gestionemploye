"""
Module contenant les exceptions personnalisées pour l'application de gestion des employés et des départements.
"""


class ApplicationError(Exception):
    """
    Classe de base pour toutes les exceptions personnalisées de l'application.
    """
    pass


class SalaireInvalideError(ApplicationError):
    """
    Exception levée lorsque le salaire saisi est négatif ou invalide.
    """
    def __init__(self, message: str = "Le salaire ne peut pas être négatif."):
        super().__init__(message)


class AgeInvalideError(ApplicationError):
    """
    Exception levée lorsque l'âge saisi est hors des limites valides.
    """
    def __init__(self, message: str = "L'âge doit être compris entre 18 et 100 ans."):
        super().__init__(message)


class MatriculeInexistantError(ApplicationError):
    """
    Exception levée lorsqu'un matricule d'employé est recherché mais n'existe pas.
    """
    def __init__(self, matricule: str):
        super().__init__(f"Aucun employé n'a été trouvé avec le matricule '{matricule}'.")


class DepartementIntrouvableError(ApplicationError):
    """
    Exception levée lorsqu'un code de département est introuvable.
    """
    def __init__(self, code: str):
        super().__init__(f"Aucun département n'a été trouvé avec le code '{code}'.")


class FichierErreur(ApplicationError):
    """
    Exception levée lors des erreurs de lecture ou d'écriture dans les fichiers JSON.
    """
    def __init__(self, message: str):
        super().__init__(f"Erreur de gestion de fichier : {message}")
