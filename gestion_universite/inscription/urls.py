"""
Configuration des URLs de l'application inscription.

Définit les routes pour toutes les opérations CRUD
sur les étudiants et les cours.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.AccueilView.as_view(), name='accueil'),

    # ── URLs des Étudiants ──
    path(
        'etudiants/',
        views.EtudiantListeView.as_view(),
        name='etudiant_liste'
    ),
    path(
        'etudiants/<int:pk>/',
        views.EtudiantDetailView.as_view(),
        name='etudiant_detail'
    ),
    path(
        'etudiants/creer/',
        views.EtudiantCreerView.as_view(),
        name='etudiant_creer'
    ),
    path(
        'etudiants/<int:pk>/modifier/',
        views.EtudiantModifierView.as_view(),
        name='etudiant_modifier'
    ),
    path(
        'etudiants/<int:pk>/supprimer/',
        views.EtudiantSupprimerView.as_view(),
        name='etudiant_supprimer'
    ),

    # ── URLs des Cours ──
    path(
        'cours/',
        views.CoursListeView.as_view(),
        name='cours_liste'
    ),
    path(
        'cours/<int:pk>/',
        views.CoursDetailView.as_view(),
        name='cours_detail'
    ),
    path(
        'cours/creer/',
        views.CoursCreerView.as_view(),
        name='cours_creer'
    ),
    path(
        'cours/<int:pk>/modifier/',
        views.CoursModifierView.as_view(),
        name='cours_modifier'
    ),
    path(
        'cours/<int:pk>/supprimer/',
        views.CoursSupprimerView.as_view(),
        name='cours_supprimer'
    ),
]
