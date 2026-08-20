# 🏢 Application de Gestion des Employés et des Départements (Python POO & Console)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Context & Objectives

Une entreprise souhaite développer une application permettant de gérer ses employés et leurs départements. Cette application a été conçue et développée en respectant scrupuleusement les **bonnes pratiques de développement logiciel Orienté Objet (POO)**, la **gestion robuste des exceptions** et la **persistance des données au format JSON**.

L'application s'exécute en mode console (Terminal) et propose un menu interactif complet.

### 🎯 Objectifs pédagogiques & techniques validés
- **Programmation Orientée Objet (POO)** : Héritage, Encapsulation et Polymorphisme.
- **Organisation Modulaire** : Découpage propre en fichiers spécialisés (`main.py`, `personne.py`, `employe.py`, etc.).
- **Gestion des Exceptions** : Utilisation rigoureuse de `try`, `except`, `finally`, `raise` et d'exceptions personnalisées.
- **Persistance des Données** : Lecture, écriture et rechargement automatique depuis des fichiers JSON (`employes.json` et `departements.json`).
- **Documentation Complete** : Présence de Docstrings sur l'intégralité des classes et méthodes du projet.

---

## ⚙️ Architecture du Projet

```text
ProjetGestionEmployes/
│── main.py                   # Point d'entrée principal & Menu interactif
│── personne.py               # Classe de base Personne (Encapsulation, Age validation)
│── employe.py                # Classe Employe (Hérite de Personne, Salaire validation)
│── departement.py            # Classe Departement (Code, Nom, Description)
│── gestion_employes.py       # Classe GestionEmployes (CRUD, Stats, Persistance JSON)
│── gestion_departements.py   # Classe GestionDepartements (CRUD, Persistance JSON)
│── exceptions.py             # Exceptions personnalisées de l'application
│── utils.py                  # Fonctions d'entrées/sorties sécurisées et formatage console
│── test_system.py            # Suite de tests unitaires automatisés
│── employes.json             # Fichier de persistance JSON des employés
│── departements.json         # Fichier de persistance JSON des départements
└── README.md                 # Documentation du projet
```

---

## 🧠 Notions POO et Choix de Conception

### 1. Encapsulation
Tous les attributs des classes (`Personne`, `Employe`, `Departement`) sont définis comme privés (préfixés par `_`). L'accès et la modification s'effectuent exclusivement via des propriétés Python (`@property` et `@<attribut>.setter`).
Les vérifications d'intégrité (ex: âge >= 18, salaire >= 0) sont appliquées directement dans les setters.

### 2. Héritage
La classe `Employe` hérite directement de la classe `Personne` :
```python
class Employe(Personne):
    def __init__(self, matricule, nom, prenom, age, sexe, adresse, telephone, poste, salaire, departement):
        super().__init__(nom, prenom, age, sexe, adresse, telephone)
        # Attributs propres à Employe
```

### 3. Polymorphisme
La méthode `afficher()` est définie dans `Personne`, `Employe` et `Departement`. Chaque classe redéfinit cette méthode pour fournir une restitution adaptée de ses données :
- `Personne.afficher()` : Affiche l'identité générale.
- `Employe.afficher()` : Appelle `super().afficher()` puis affiche le matricule, le poste, le salaire et le département.
- `Departement.afficher()` : Affiche le code, le nom et la description.

### 4. Gestion des Exceptions
Des classes d'exceptions personnalisées héritent de `ApplicationError` :
- `SalaireInvalideError` : Levée en cas de salaire négatif.
- `AgeInvalideError` : Levée en cas d'âge hors des bornes (18 - 100 ans).
- `MatriculeInexistantError` : Levée lors de la recherche/modification d'un matricule absent.
- `DepartementIntrouvableError` : Levée lorsqu'un code de département n'existe pas.
- `FichierErreur` : Levée lors d'erreurs d'E/S sur les fichiers JSON.

Les blocs `try...except...finally` garantissent la fermeture sécurisée des descripteurs de fichiers lors des sauvegardes et rechargements.

---

## 🚀 Fonctionnalités Détaillées

### 1. Gestion des Employés
- **Ajouter un employé** (Matricule unique, Nom, Prénom, Âge, Sexe, Adresse, Téléphone, Poste, Salaire, Département).
- **Modifier un employé** (Mise à jour sélective des champs).
- **Supprimer un employé** (Avec confirmation).
- **Rechercher un employé** par matricule.
- **Afficher la liste complète**.

### 2. Gestion des Départements
- **Ajouter un département** (Code unique, Nom, Description).
- **Modifier un département**.
- **Supprimer un département**.
- **Afficher tous les départements**.
- **Affecter un employé** à un département.

### 3. Statistiques & Analyse
- Nombre total d'employés.
- Salaire minimum, maximum et moyen.
- Masse salariale globale de l'entreprise.
- Distribution du nombre d'employés par département.

### 4. Persistance JSON
- **Rechargement automatique** au démarrage de l'application.
- **Sauvegarde automatique** lors de chaque modification et à la fermeture.
- **Sauvegarde manuelle** disponible via le menu.

---

## 💻 Installation et Exécution

### Prérequis
- Python 3.8 ou plus récent.

### Lancement de l'application
```bash
python main.py
```

### Lancement des tests automatisés
```bash
python test_system.py
```

---

## 🗂️ Guide Git & GitHub

### 1. Initialiser le dépôt local et effectuer le premier commit
```bash
git init
git add .
git commit -m "feat: Première version stable de l'application de Gestion des Employés"
```

### 2. Lier et pousser vers un dépôt GitHub distant
```bash
git branch -M main
git remote add origin https://github.com/votre-compte/ProjetGestionEmployes.git
git push -u origin main
```

---

## 👨‍💻 Auteur & Licence
Projet réalisé dans le cadre du cours de développement logiciel Python.
Licence MIT - Libre de réutilisation et de modification.
