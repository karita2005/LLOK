"""
Formulaires de l'application inscription.

Contient les formulaires ModelForm pour la création et la modification
des étudiants et des cours, avec gestion du champ ManyToMany.
"""

from django import forms
from .models import Etudiant, Cours


class EtudiantForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un étudiant.

    Le champ 'cours' utilise CheckboxSelectMultiple pour permettre
    la sélection multiple de cours via des cases à cocher.
    """

    class Meta:
        model = Etudiant
        fields = ['nom', 'prenom', 'email', 'cours']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom de famille',
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le prénom',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemple@universite.fr',
            }),
            'cours': forms.CheckboxSelectMultiple(),
        }


class CoursForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un cours.

    Tous les champs utilisent des widgets Bootstrap pour
    une présentation cohérente.
    """

    class Meta:
        model = Cours
        fields = ['nom', 'description', 'professeur']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom du cours',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le contenu du cours',
            }),
            'professeur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du professeur',
            }),
        }
