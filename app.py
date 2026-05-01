"""
Application CRUD Flask — Gestion des Étudiants et des Cours
===========================================================
Une API REST complète démontrant une relation many-to-many
entre les modèles Étudiant et Cours, avec toutes les réponses,
variables et commentaires en français.
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# ============================================================
# Configuration de l'application
# ============================================================

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///universite.db"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

base_de_donnees = SQLAlchemy(application)

# ============================================================
# Table d'association many-to-many (Étudiants ↔ Cours)
# ============================================================

inscriptions = base_de_donnees.Table(
    "inscriptions",
    base_de_donnees.Column(
        "etudiant_id",
        base_de_donnees.Integer,
        base_de_donnees.ForeignKey("etudiants.id"),
        primary_key=True,
    ),
    base_de_donnees.Column(
        "cours_id",
        base_de_donnees.Integer,
        base_de_donnees.ForeignKey("cours.id"),
        primary_key=True,
    ),
)

# ============================================================
# Modèles
# ============================================================


class Etudiant(base_de_donnees.Model):
    """Modèle représentant un étudiant inscrit à l'université."""

    __tablename__ = "etudiants"

    id = base_de_donnees.Column(base_de_donnees.Integer, primary_key=True)
    nom = base_de_donnees.Column(base_de_donnees.String(100), nullable=False)
    prenom = base_de_donnees.Column(base_de_donnees.String(100), nullable=False)
    email = base_de_donnees.Column(
        base_de_donnees.String(120), unique=True, nullable=False
    )

    # Relation many-to-many vers les cours
    cours = base_de_donnees.relationship(
        "Cours",
        secondary=inscriptions,
        backref=base_de_donnees.backref("etudiants", lazy="dynamic"),
        lazy="dynamic",
    )

    def en_dictionnaire(self):
        """Convertit l'objet en dictionnaire pour la sérialisation JSON."""
        return {
            "id": self.id,
            "nom": self.nom,
            "prénom": self.prenom,
            "email": self.email,
            "cours": [
                {"id": c.id, "nom": c.nom} for c in self.cours
            ],
        }


class Cours(base_de_donnees.Model):
    """Modèle représentant un cours proposé par l'université."""

    __tablename__ = "cours"

    id = base_de_donnees.Column(base_de_donnees.Integer, primary_key=True)
    nom = base_de_donnees.Column(base_de_donnees.String(150), nullable=False)
    description = base_de_donnees.Column(base_de_donnees.Text, nullable=True)
    professeur = base_de_donnees.Column(base_de_donnees.String(100), nullable=False)

    def en_dictionnaire(self):
        """Convertit l'objet en dictionnaire pour la sérialisation JSON."""
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "professeur": self.professeur,
            "étudiants": [
                {"id": e.id, "nom": e.nom, "prénom": e.prenom}
                for e in self.etudiants
            ],
        }


# ============================================================
# Fonctions utilitaires
# ============================================================


def reponse_erreur(message, code_statut):
    """Renvoie une réponse JSON d'erreur normalisée."""
    return jsonify({"erreur": message}), code_statut


# ============================================================
# Routes — Étudiants
# ============================================================


# Récupérer la liste de tous les étudiants
@application.route("/api/etudiants", methods=["GET"])
def obtenir_etudiants():
    """Renvoie la liste complète des étudiants."""
    etudiants = Etudiant.query.all()
    return jsonify({
        "message": "Liste des étudiants récupérée avec succès",
        "données": [e.en_dictionnaire() for e in etudiants],
        "total": len(etudiants),
    })


# Récupérer un étudiant par son identifiant
@application.route("/api/etudiants/<int:identifiant>", methods=["GET"])
def obtenir_etudiant(identifiant):
    """Renvoie les détails d'un étudiant donné."""
    etudiant = base_de_donnees.session.get(Etudiant, identifiant)
    if etudiant is None:
        return reponse_erreur("Étudiant non trouvé", 404)
    return jsonify({
        "message": "Étudiant récupéré avec succès",
        "données": etudiant.en_dictionnaire(),
    })


# Créer un nouvel étudiant
@application.route("/api/etudiants", methods=["POST"])
def creer_etudiant():
    """Crée un nouvel étudiant à partir des données JSON fournies."""
    donnees = request.get_json()
    if not donnees:
        return reponse_erreur("Aucune donnée JSON fournie", 400)

    champs_requis = ["nom", "prenom", "email"]
    for champ in champs_requis:
        if champ not in donnees or not donnees[champ]:
            return reponse_erreur(f"Le champ '{champ}' est obligatoire", 400)

    # Vérifier l'unicité de l'email
    existant = Etudiant.query.filter_by(email=donnees["email"]).first()
    if existant:
        return reponse_erreur("Un étudiant avec cet email existe déjà", 400)

    nouvel_etudiant = Etudiant(
        nom=donnees["nom"],
        prenom=donnees["prenom"],
        email=donnees["email"],
    )
    base_de_donnees.session.add(nouvel_etudiant)
    base_de_donnees.session.commit()

    return jsonify({
        "message": "Étudiant créé avec succès",
        "données": nouvel_etudiant.en_dictionnaire(),
    }), 201


# Mettre à jour un étudiant existant
@application.route("/api/etudiants/<int:identifiant>", methods=["PUT"])
def modifier_etudiant(identifiant):
    """Met à jour les informations d'un étudiant existant."""
    etudiant = base_de_donnees.session.get(Etudiant, identifiant)
    if etudiant is None:
        return reponse_erreur("Étudiant non trouvé", 404)

    donnees = request.get_json()
    if not donnees:
        return reponse_erreur("Aucune donnée JSON fournie", 400)

    # Vérifier l'unicité de l'email si modifié
    if "email" in donnees and donnees["email"] != etudiant.email:
        existant = Etudiant.query.filter_by(email=donnees["email"]).first()
        if existant:
            return reponse_erreur("Un étudiant avec cet email existe déjà", 400)

    etudiant.nom = donnees.get("nom", etudiant.nom)
    etudiant.prenom = donnees.get("prenom", etudiant.prenom)
    etudiant.email = donnees.get("email", etudiant.email)

    base_de_donnees.session.commit()

    return jsonify({
        "message": "Étudiant mis à jour avec succès",
        "données": etudiant.en_dictionnaire(),
    })


# Supprimer un étudiant
@application.route("/api/etudiants/<int:identifiant>", methods=["DELETE"])
def supprimer_etudiant(identifiant):
    """Supprime un étudiant de la base de données."""
    etudiant = base_de_donnees.session.get(Etudiant, identifiant)
    if etudiant is None:
        return reponse_erreur("Étudiant non trouvé", 404)

    base_de_donnees.session.delete(etudiant)
    base_de_donnees.session.commit()

    return jsonify({"message": "Étudiant supprimé avec succès"})


# ============================================================
# Routes — Cours
# ============================================================


# Récupérer la liste de tous les cours
@application.route("/api/cours", methods=["GET"])
def obtenir_cours():
    """Renvoie la liste complète des cours disponibles."""
    liste_cours = Cours.query.all()
    return jsonify({
        "message": "Liste des cours récupérée avec succès",
        "données": [c.en_dictionnaire() for c in liste_cours],
        "total": len(liste_cours),
    })


# Récupérer un cours par son identifiant
@application.route("/api/cours/<int:identifiant>", methods=["GET"])
def obtenir_un_cours(identifiant):
    """Renvoie les détails d'un cours donné."""
    cours = base_de_donnees.session.get(Cours, identifiant)
    if cours is None:
        return reponse_erreur("Cours non trouvé", 404)
    return jsonify({
        "message": "Cours récupéré avec succès",
        "données": cours.en_dictionnaire(),
    })


# Créer un nouveau cours
@application.route("/api/cours", methods=["POST"])
def creer_cours():
    """Crée un nouveau cours à partir des données JSON fournies."""
    donnees = request.get_json()
    if not donnees:
        return reponse_erreur("Aucune donnée JSON fournie", 400)

    champs_requis = ["nom", "professeur"]
    for champ in champs_requis:
        if champ not in donnees or not donnees[champ]:
            return reponse_erreur(f"Le champ '{champ}' est obligatoire", 400)

    nouveau_cours = Cours(
        nom=donnees["nom"],
        description=donnees.get("description", ""),
        professeur=donnees["professeur"],
    )
    base_de_donnees.session.add(nouveau_cours)
    base_de_donnees.session.commit()

    return jsonify({
        "message": "Cours créé avec succès",
        "données": nouveau_cours.en_dictionnaire(),
    }), 201


# Mettre à jour un cours existant
@application.route("/api/cours/<int:identifiant>", methods=["PUT"])
def modifier_cours(identifiant):
    """Met à jour les informations d'un cours existant."""
    cours = base_de_donnees.session.get(Cours, identifiant)
    if cours is None:
        return reponse_erreur("Cours non trouvé", 404)

    donnees = request.get_json()
    if not donnees:
        return reponse_erreur("Aucune donnée JSON fournie", 400)

    cours.nom = donnees.get("nom", cours.nom)
    cours.description = donnees.get("description", cours.description)
    cours.professeur = donnees.get("professeur", cours.professeur)

    base_de_donnees.session.commit()

    return jsonify({
        "message": "Cours mis à jour avec succès",
        "données": cours.en_dictionnaire(),
    })


# Supprimer un cours
@application.route("/api/cours/<int:identifiant>", methods=["DELETE"])
def supprimer_cours(identifiant):
    """Supprime un cours de la base de données."""
    cours = base_de_donnees.session.get(Cours, identifiant)
    if cours is None:
        return reponse_erreur("Cours non trouvé", 404)

    base_de_donnees.session.delete(cours)
    base_de_donnees.session.commit()

    return jsonify({"message": "Cours supprimé avec succès"})


# ============================================================
# Routes — Gestion des inscriptions (association many-to-many)
# ============================================================


# Inscrire un étudiant à un cours
@application.route(
    "/api/etudiants/<int:id_etudiant>/inscrire/<int:id_cours>", methods=["POST"]
)
def inscrire_etudiant(id_etudiant, id_cours):
    """Inscrit un étudiant à un cours (ajoute l'association)."""
    etudiant = base_de_donnees.session.get(Etudiant, id_etudiant)
    if etudiant is None:
        return reponse_erreur("Étudiant non trouvé", 404)

    cours = base_de_donnees.session.get(Cours, id_cours)
    if cours is None:
        return reponse_erreur("Cours non trouvé", 404)

    # Vérifier si l'étudiant est déjà inscrit à ce cours
    if cours in etudiant.cours.all():
        return reponse_erreur("L'étudiant est déjà inscrit à ce cours", 400)

    etudiant.cours.append(cours)
    base_de_donnees.session.commit()

    return jsonify({
        "message": f"{etudiant.prenom} {etudiant.nom} a été inscrit(e) au cours « {cours.nom} »",
        "données": etudiant.en_dictionnaire(),
    }), 201


# Désinscrire un étudiant d'un cours
@application.route(
    "/api/etudiants/<int:id_etudiant>/desinscrire/<int:id_cours>", methods=["DELETE"]
)
def desinscrire_etudiant(id_etudiant, id_cours):
    """Désinscrit un étudiant d'un cours (supprime l'association)."""
    etudiant = base_de_donnees.session.get(Etudiant, id_etudiant)
    if etudiant is None:
        return reponse_erreur("Étudiant non trouvé", 404)

    cours = base_de_donnees.session.get(Cours, id_cours)
    if cours is None:
        return reponse_erreur("Cours non trouvé", 404)

    # Vérifier si l'étudiant est inscrit à ce cours
    if cours not in etudiant.cours.all():
        return reponse_erreur("L'étudiant n'est pas inscrit à ce cours", 400)

    etudiant.cours.remove(cours)
    base_de_donnees.session.commit()

    return jsonify({
        "message": f"{etudiant.prenom} {etudiant.nom} a été désinscrit(e) du cours « {cours.nom} »",
        "données": etudiant.en_dictionnaire(),
    })


# Récupérer les cours d'un étudiant donné
@application.route("/api/etudiants/<int:identifiant>/cours", methods=["GET"])
def obtenir_cours_etudiant(identifiant):
    """Renvoie la liste des cours auxquels un étudiant est inscrit."""
    etudiant = base_de_donnees.session.get(Etudiant, identifiant)
    if etudiant is None:
        return reponse_erreur("Étudiant non trouvé", 404)

    liste_cours = [{"id": c.id, "nom": c.nom, "professeur": c.professeur} for c in etudiant.cours]
    return jsonify({
        "message": f"Cours de {etudiant.prenom} {etudiant.nom}",
        "données": liste_cours,
        "total": len(liste_cours),
    })


# Récupérer les étudiants inscrits à un cours donné
@application.route("/api/cours/<int:identifiant>/etudiants", methods=["GET"])
def obtenir_etudiants_cours(identifiant):
    """Renvoie la liste des étudiants inscrits à un cours."""
    cours = base_de_donnees.session.get(Cours, identifiant)
    if cours is None:
        return reponse_erreur("Cours non trouvé", 404)

    liste_etudiants = [
        {"id": e.id, "nom": e.nom, "prénom": e.prenom} for e in cours.etudiants
    ]
    return jsonify({
        "message": f"Étudiants inscrits au cours « {cours.nom} »",
        "données": liste_etudiants,
        "total": len(liste_etudiants),
    })


# ============================================================
# Peuplement de la base de données avec des données d'exemple
# ============================================================


def peupler_base_de_donnees():
    """Insère des données d'exemple françaises dans la base de données."""

    # Données d'exemple — Étudiants
    etudiants_exemple = [
        Etudiant(nom="Dupont", prenom="Marie", email="marie.dupont@universite.fr"),
        Etudiant(nom="Martin", prenom="Jean", email="jean.martin@universite.fr"),
        Etudiant(nom="Bernard", prenom="Sophie", email="sophie.bernard@universite.fr"),
        Etudiant(nom="Petit", prenom="Lucas", email="lucas.petit@universite.fr"),
        Etudiant(nom="Moreau", prenom="Camille", email="camille.moreau@universite.fr"),
    ]

    # Données d'exemple — Cours
    cours_exemple = [
        Cours(
            nom="Mathématiques Avancées",
            description="Cours couvrant l'algèbre linéaire, le calcul différentiel et intégral.",
            professeur="Pr. Lefebvre",
        ),
        Cours(
            nom="Littérature Française",
            description="Étude des grands auteurs français du XIXe et XXe siècle.",
            professeur="Pr. Dubois",
        ),
        Cours(
            nom="Informatique Fondamentale",
            description="Introduction aux algorithmes, structures de données et programmation.",
            professeur="Pr. Garnier",
        ),
        Cours(
            nom="Philosophie Moderne",
            description="Exploration des courants philosophiques de Descartes à Sartre.",
            professeur="Pr. Rousseau",
        ),
    ]

    for etudiant in etudiants_exemple:
        base_de_donnees.session.add(etudiant)
    for cours in cours_exemple:
        base_de_donnees.session.add(cours)

    base_de_donnees.session.commit()

    # Inscrire des étudiants à des cours pour illustrer la relation
    etudiants_exemple[0].cours.append(cours_exemple[0])  # Marie → Maths
    etudiants_exemple[0].cours.append(cours_exemple[1])  # Marie → Littérature
    etudiants_exemple[1].cours.append(cours_exemple[0])  # Jean → Maths
    etudiants_exemple[1].cours.append(cours_exemple[2])  # Jean → Informatique
    etudiants_exemple[2].cours.append(cours_exemple[1])  # Sophie → Littérature
    etudiants_exemple[2].cours.append(cours_exemple[3])  # Sophie → Philosophie
    etudiants_exemple[3].cours.append(cours_exemple[2])  # Lucas → Informatique
    etudiants_exemple[3].cours.append(cours_exemple[0])  # Lucas → Maths
    etudiants_exemple[4].cours.append(cours_exemple[3])  # Camille → Philosophie
    etudiants_exemple[4].cours.append(cours_exemple[1])  # Camille → Littérature

    base_de_donnees.session.commit()
    print("✓ Base de données peuplée avec les données d'exemple.")


# ============================================================
# Point d'entrée
# ============================================================

if __name__ == "__main__":
    with application.app_context():
        base_de_donnees.create_all()
        # Peupler uniquement si la base est vide
        if Etudiant.query.count() == 0:
            peupler_base_de_donnees()
    application.run(debug=True, host="0.0.0.0", port=5000)
