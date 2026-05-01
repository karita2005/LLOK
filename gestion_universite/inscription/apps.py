"""Configuration de l'application inscription."""

from django.apps import AppConfig


class InscriptionConfig(AppConfig):
    """Configuration de l'application de gestion des inscriptions."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inscription'
    verbose_name = 'Gestion des inscriptions'
