"""
Module d'utilitaires pour la saisie sécurisée et le formatage d'affichage dans la console.
"""

from typing import Optional


def saisir_chaine(invite: str, obligatoire: bool = True, valeur_defaut: str = "") -> str:
    """
    Demande une chaîne de caractères à l'utilisateur.

    Args:
        invite (str): Message d'invite à afficher.
        obligatoire (bool): Si True, la saisie ne peut pas être vide.
        valeur_defaut (str): Valeur par défaut si non obligatoire et vide.

    Returns:
        str: La chaîne saisie et nettoyée.
    """
    while True:
        saisie = input(invite).strip()
        if not saisie:
            if not obligatoire:
                return valeur_defaut
            print("❌ Erreur : Ce champ ne peut pas être vide. Veuillez réesseyer.")
        else:
            return saisie


def saisir_entier(invite: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """
    Demande la saisie d'un nombre entier valide avec gestion du try...except.

    Args:
        invite (str): Message d'invite.
        min_val (int, optional): Valeur minimale autorisée.
        max_val (int, optional): Valeur maximale autorisée.

    Returns:
        int: L'entier validé.
    """
    while True:
        saisie = input(invite).strip()
        try:
            valeur = int(saisie)
            if min_val is not None and valeur < min_val:
                print(f"❌ Erreur : La valeur doit être au moins de {min_val}.")
                continue
            if max_val is not None and valeur > max_val:
                print(f"❌ Erreur : La valeur ne peut pas dépasser {max_val}.")
                continue
            return valeur
        except ValueError:
            print("❌ Erreur : Veuillez saisir un nombre entier valide.")


def saisir_flottant(invite: str, min_val: Optional[float] = None) -> float:
    """
    Demande la saisie d'un nombre décimal (float) valide avec gestion du try...except.

    Args:
        invite (str): Message d'invite.
        min_val (float, optional): Valeur minimale autorisée.

    Returns:
        float: Le nombre décimal validé.
    """
    while True:
        saisie = input(invite).strip()
        try:
            valeur = float(saisie)
            if min_val is not None and valeur < min_val:
                print(f"❌ Erreur : La valeur doit être supérieure ou égale à {min_val}.")
                continue
            return valeur
        except ValueError:
            print("❌ Erreur : Veuillez saisir un nombre décimal valide.")


def confirmer_action(invite: str) -> bool:
    """
    Demande une confirmation (O/N) à l'utilisateur.

    Args:
        invite (str): Message de confirmation.

    Returns:
        bool: True si l'utilisateur valide (O ou oui), False sinon.
    """
    reponse = input(f"{invite} (O/N) : ").strip().lower()
    return reponse in ["o", "oui", "y", "yes"]


def afficher_titre(titre: str) -> None:
    """
    Affiche un titre de section bien formaté.

    Args:
        titre (str): Le titre à afficher.
    """
    largeur = 50
    print("\n" + "=" * largeur)
    print(titre.center(largeur))
    print("=" * largeur)
