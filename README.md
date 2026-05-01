# 🎓 API CRUD — Gestion Université (Étudiants & Cours)

Application Flask complète implémentant une relation **many-to-many** entre les modèles **Étudiant** et **Cours**, avec une API REST entièrement en français.

## Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/karita2005/LLOK.git
cd LLOK

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sous Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

## Lancement de l'application

```bash
python app.py
```

L'application démarre sur `http://localhost:5000`. La base de données SQLite (`universite.db`) est créée automatiquement et peuplée avec des données d'exemple au premier lancement.

---

## Points de terminaison de l'API

### Étudiants

| Méthode  | URL                              | Description                          |
|----------|----------------------------------|--------------------------------------|
| `GET`    | `/api/etudiants`                 | Lister tous les étudiants            |
| `GET`    | `/api/etudiants/<id>`            | Récupérer un étudiant par son ID     |
| `POST`   | `/api/etudiants`                 | Créer un nouvel étudiant             |
| `PUT`    | `/api/etudiants/<id>`            | Modifier un étudiant existant        |
| `DELETE` | `/api/etudiants/<id>`            | Supprimer un étudiant                |

#### Exemple — Créer un étudiant

```bash
curl -X POST http://localhost:5000/api/etudiants \
  -H "Content-Type: application/json" \
  -d '{"nom": "Leroy", "prenom": "Antoine", "email": "antoine.leroy@universite.fr"}'
```

### Cours

| Méthode  | URL                              | Description                          |
|----------|----------------------------------|--------------------------------------|
| `GET`    | `/api/cours`                     | Lister tous les cours                |
| `GET`    | `/api/cours/<id>`                | Récupérer un cours par son ID        |
| `POST`   | `/api/cours`                     | Créer un nouveau cours               |
| `PUT`    | `/api/cours/<id>`                | Modifier un cours existant           |
| `DELETE` | `/api/cours/<id>`                | Supprimer un cours                   |

#### Exemple — Créer un cours

```bash
curl -X POST http://localhost:5000/api/cours \
  -H "Content-Type: application/json" \
  -d '{"nom": "Chimie Organique", "description": "Les bases de la chimie organique.", "professeur": "Pr. Lambert"}'
```

### Inscriptions (relation many-to-many)

| Méthode  | URL                                                    | Description                                    |
|----------|--------------------------------------------------------|------------------------------------------------|
| `POST`   | `/api/etudiants/<id_etudiant>/inscrire/<id_cours>`     | Inscrire un étudiant à un cours                |
| `DELETE` | `/api/etudiants/<id_etudiant>/desinscrire/<id_cours>`  | Désinscrire un étudiant d'un cours             |
| `GET`    | `/api/etudiants/<id>/cours`                            | Lister les cours d'un étudiant                 |
| `GET`    | `/api/cours/<id>/etudiants`                            | Lister les étudiants inscrits à un cours       |

#### Exemple — Inscrire un étudiant à un cours

```bash
curl -X POST http://localhost:5000/api/etudiants/1/inscrire/3
```

---

## Structure du projet

```
LLOK/
├── app.py              # Application principale (modèles, routes, peuplement)
├── requirements.txt    # Dépendances Python
├── README.md           # Ce fichier
└── instance/
    └── universite.db   # Base de données SQLite (créée automatiquement)
```

## Données d'exemple

Au premier lancement, la base est peuplée avec :

- **5 étudiants** : Marie Dupont, Jean Martin, Sophie Bernard, Lucas Petit, Camille Moreau
- **4 cours** : Mathématiques Avancées, Littérature Française, Informatique Fondamentale, Philosophie Moderne
- **10 inscriptions** reliant les étudiants aux cours

## Technologies utilisées

- **Flask** — Micro-framework web Python
- **Flask-SQLAlchemy** — ORM pour la gestion de la base de données
- **SQLite** — Base de données embarquée
