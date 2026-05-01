"""
Vues de l'application inscription.

Fournit les vues CRUD complètes (liste, détail, créer, modifier, supprimer)
pour les modèles Étudiant et Cours, en utilisant les vues basées sur les classes.
"""

from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.views.generic.base import TemplateView

from .models import Etudiant, Cours
from .forms import EtudiantForm, CoursForm


# ──────────────────────────────────────────────
# Page d'accueil
# ──────────────────────────────────────────────

class AccueilView(TemplateView):
    """Vue de la page d'accueil du site."""

    template_name = 'inscription/accueil.html'


# ──────────────────────────────────────────────
# Vues CRUD pour le modèle Étudiant
# ──────────────────────────────────────────────

class EtudiantListeView(ListView):
    """Affiche la liste de tous les étudiants."""

    model = Etudiant
    template_name = 'inscription/etudiant_liste.html'
    context_object_name = 'etudiants'


class EtudiantDetailView(DetailView):
    """Affiche les détails d'un étudiant avec ses cours inscrits."""

    model = Etudiant
    template_name = 'inscription/etudiant_detail.html'
    context_object_name = 'etudiant'


class EtudiantCreerView(CreateView):
    """Formulaire de création d'un nouvel étudiant."""

    model = Etudiant
    form_class = EtudiantForm
    template_name = 'inscription/etudiant_form.html'
    success_url = reverse_lazy('etudiant_liste')

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['titre'] = 'Ajouter un étudiant'
        contexte['bouton'] = 'Créer'
        return contexte


class EtudiantModifierView(UpdateView):
    """Formulaire de modification d'un étudiant existant."""

    model = Etudiant
    form_class = EtudiantForm
    template_name = 'inscription/etudiant_form.html'
    success_url = reverse_lazy('etudiant_liste')

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['titre'] = 'Modifier l\'étudiant'
        contexte['bouton'] = 'Enregistrer'
        return contexte


class EtudiantSupprimerView(DeleteView):
    """Confirmation et suppression d'un étudiant."""

    model = Etudiant
    template_name = 'inscription/etudiant_confirmer_suppression.html'
    context_object_name = 'etudiant'
    success_url = reverse_lazy('etudiant_liste')


# ──────────────────────────────────────────────
# Vues CRUD pour le modèle Cours
# ──────────────────────────────────────────────

class CoursListeView(ListView):
    """Affiche la liste de tous les cours disponibles."""

    model = Cours
    template_name = 'inscription/cours_liste.html'
    context_object_name = 'cours_liste'


class CoursDetailView(DetailView):
    """Affiche les détails d'un cours avec la liste des étudiants inscrits."""

    model = Cours
    template_name = 'inscription/cours_detail.html'
    context_object_name = 'cours'


class CoursCreerView(CreateView):
    """Formulaire de création d'un nouveau cours."""

    model = Cours
    form_class = CoursForm
    template_name = 'inscription/cours_form.html'
    success_url = reverse_lazy('cours_liste')

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['titre'] = 'Ajouter un cours'
        contexte['bouton'] = 'Créer'
        return contexte


class CoursModifierView(UpdateView):
    """Formulaire de modification d'un cours existant."""

    model = Cours
    form_class = CoursForm
    template_name = 'inscription/cours_form.html'
    success_url = reverse_lazy('cours_liste')

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['titre'] = 'Modifier le cours'
        contexte['bouton'] = 'Enregistrer'
        return contexte


class CoursSupprimerView(DeleteView):
    """Confirmation et suppression d'un cours."""

    model = Cours
    template_name = 'inscription/cours_confirmer_suppression.html'
    context_object_name = 'cours'
    success_url = reverse_lazy('cours_liste')
