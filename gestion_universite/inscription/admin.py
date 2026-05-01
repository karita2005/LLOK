"""
Configuration de l'interface d'administration Django
pour les modèles Étudiant et Cours.
"""

from django.contrib import admin
from .models import Etudiant, Cours


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    """Administration du modèle Cours."""

    list_display = ('nom', 'professeur', 'date_creation')
    search_fields = ('nom', 'professeur')


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    """Administration du modèle Étudiant."""

    list_display = ('nom', 'prenom', 'email', 'date_inscription')
    search_fields = ('nom', 'prenom', 'email')
    filter_horizontal = ('cours',)
