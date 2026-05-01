# Gestion Université — Étudiants & Cours

Ce dépôt contient deux applications de gestion universitaire implémentant une relation **many-to-many** entre les modèles **Étudiant** et **Cours**, entièrement en français.

---

## Application Django CRUD (avec interface Bootstrap 5)

Application web complète avec interface graphique Bootstrap 5, offrant toutes les opérations CRUD via des formulaires et des vues.

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation et lancement

```bash
# 1. Cloner le dépôt
git clone https://github.com/karita2005/LLOK.git
cd LLOK

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sous Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer les migrations et appliquer
cd gestion_universite
python manage.py makemigrations
python manage.py migrate

# 5. Lancer le serveur de développement
python manage.py runserver
```

L'application Django démarre sur `http://localhost:8000`.

### Structure du projet Django

```
gestion_universite/
├── manage.py                          # Utilitaire en ligne de commande Django
├── gestion_universite/
│   ├── __init__.py
│   ├── settings.py                    # Configuration du projet (SQLite, apps, templates)
│   ├── urls.py                        # URLs principales
│   └── wsgi.py                        # Point d'entrée WSGI
└── inscription/
    ├── __init__.py
    ├── admin.py                       # Configuration de l'admin Django
    ├── apps.py                        # Configuration de l'application
    ├── forms.py                       # Formulaires ModelForm (CheckboxSelectMultiple)
    ├── models.py                      # Modèles Étudiant et Cours (ManyToManyField)
    ├── urls.py                        # URLs de l'application
    ├── views.py                       # Vues CRUD (class-based views)
    ├── migrations/
    │   └── 0001_initial.py            # Migration initiale
    └── templates/inscription/
        ├── base.html                  # Template de base (navbar, Bootstrap 5)
        ├── accueil.html               # Page d'accueil
        ├── etudiant_liste.html        # Liste des étudiants
        ├── etudiant_detail.html       # Détail d'un étudiant
        ├── etudiant_form.html         # Formulaire création/modification étudiant
        ├── etudiant_confirmer_suppression.html  # Confirmation suppression
        ├── cours_liste.html           # Liste des cours
        ├── cours_detail.html          # Détail d'un cours
        ├── cours_form.html            # Formulaire création/modification cours
        └── cours_confirmer_suppression.html     # Confirmation suppression
```

### URLs disponibles (Django)

| URL                              | Description                              |
|----------------------------------|------------------------------------------|
| `/`                              | Page d'accueil                           |
| `/etudiants/`                    | Liste des étudiants                      |
| `/etudiants/creer/`              | Créer un étudiant                        |
| `/etudiants/<id>/`               | Détail d'un étudiant                     |
| `/etudiants/<id>/modifier/`      | Modifier un étudiant                     |
| `/etudiants/<id>/supprimer/`     | Supprimer un étudiant                    |
| `/cours/`                        | Liste des cours                          |
| `/cours/creer/`                  | Créer un cours                           |
| `/cours/<id>/`                   | Détail d'un cours                        |
| `/cours/<id>/modifier/`          | Modifier un cours                        |
| `/cours/<id>/supprimer/`         | Supprimer un cours                       |
| `/admin/`                        | Interface d'administration Django        |

### Fonctionnalités

- **Modèles** : `Etudiant` et `Cours` avec `ManyToManyField`
- **Vues** : Class-based views (ListView, DetailView, CreateView, UpdateView, DeleteView)
- **Formulaires** : `ModelForm` avec `CheckboxSelectMultiple` pour le champ many-to-many
- **Templates** : Bootstrap 5 avec icônes Bootstrap Icons
- **Administration** : Interface admin Django configurée

---

## API REST Flask

Application Flask avec API REST pour les mêmes modèles.

### Lancement de l'API Flask

```bash
cd LLOK
python app.py
```

L'application démarre sur `http://localhost:5000`.

### Points de terminaison de l'API

#### Étudiants

| Méthode  | URL                              | Description                          |
|----------|----------------------------------|--------------------------------------|
| `GET`    | `/api/etudiants`                 | Lister tous les étudiants            |
| `GET`    | `/api/etudiants/<id>`            | Récupérer un étudiant par son ID     |
| `POST`   | `/api/etudiants`                 | Créer un nouvel étudiant             |
| `PUT`    | `/api/etudiants/<id>`            | Modifier un étudiant existant        |
| `DELETE` | `/api/etudiants/<id>`            | Supprimer un étudiant                |

#### Cours

| Méthode  | URL                              | Description                          |
|----------|----------------------------------|--------------------------------------|
| `GET`    | `/api/cours`                     | Lister tous les cours                |
| `GET`    | `/api/cours/<id>`                | Récupérer un cours par son ID        |
| `POST`   | `/api/cours`                     | Créer un nouveau cours               |
| `PUT`    | `/api/cours/<id>`                | Modifier un cours existant           |
| `DELETE` | `/api/cours/<id>`                | Supprimer un cours                   |

#### Inscriptions (relation many-to-many)

| Méthode  | URL                                                    | Description                                    |
|----------|--------------------------------------------------------|------------------------------------------------|
| `POST`   | `/api/etudiants/<id_etudiant>/inscrire/<id_cours>`     | Inscrire un étudiant à un cours                |
| `DELETE` | `/api/etudiants/<id_etudiant>/desinscrire/<id_cours>`  | Désinscrire un étudiant d'un cours             |
| `GET`    | `/api/etudiants/<id>/cours`                            | Lister les cours d'un étudiant                 |
| `GET`    | `/api/cours/<id>/etudiants`                            | Lister les étudiants inscrits à un cours       |

---

## Technologies utilisées

- **Django** — Framework web Python (application CRUD avec Bootstrap 5)
- **Flask** — Micro-framework web Python (API REST)
- **Flask-SQLAlchemy** — ORM pour Flask
- **SQLite** — Base de données embarquée
- **Bootstrap 5** — Framework CSS pour l'interface utilisateur
