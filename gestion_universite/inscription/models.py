"""
Modèles de l'application inscription.

Définit les modèles Étudiant et Cours avec une relation ManyToMany
pour gérer les inscriptions des étudiants aux différents cours.
"""

from django.db import models


class Cours(models.Model):
    """
    Modèle représentant un cours universitaire.

    Attributs :
        nom : Nom du cours
        description : Description détaillée du cours
        professeur : Nom du professeur responsable
        date_creation : Date de création automatique de l'enregistrement
    """

    nom = models.CharField(
        max_length=200,
        verbose_name="Nom du cours"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    professeur = models.CharField(
        max_length=200,
        verbose_name="Professeur"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Etudiant(models.Model):
    """
    Modèle représentant un étudiant.

    Attributs :
        nom : Nom de famille de l'étudiant
        prenom : Prénom de l'étudiant
        email : Adresse e-mail unique de l'étudiant
        cours : Relation ManyToMany vers les cours auxquels l'étudiant est inscrit
        date_inscription : Date d'inscription automatique
    """

    nom = models.CharField(
        max_length=100,
        verbose_name="Nom"
    )
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Adresse e-mail"
    )
    cours = models.ManyToManyField(
        Cours,
        blank=True,
        related_name='etudiants',
        verbose_name="Cours inscrits"
    )
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"
